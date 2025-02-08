<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { Ref } from 'vue';
import type { IRule, IMatch, IJSONAPIResource } from '@/types';
import { RuleRepository } from '@/repositories/rule';
import moment from 'moment';
import { isPropertySignature } from 'typescript';

const rules: Ref<IJSONAPIResource<IRule>[]> = ref([]);
const matches: Ref<IJSONAPIResource<IMatch[]> | undefined> = ref<IJSONAPIResource<IMatch[]>>();

const rule_columns = [
  { name: 'name', align: 'center', label: 'Name', field: (row: IJSONAPIResource<IRule>) => row.attributes?.name, sortable: true },
  { name: 'created_at', align: 'center', label: 'Created At', field: (row: IJSONAPIResource<IRule>) => row.attributes?.created_at, sortable: true },
  { name: 'content_type', align: 'center', label: 'Content Type', field: (row: IJSONAPIResource<IRule>) => row.attributes?.content_type, sortable: true }
];

const rule_pagination = {
  rowsPerPage: 20,
  sortBy: "created_at",
  descending: true
}

const match_columns = [
  { name: 'invert', align: 'center', label: 'Invert', field: (row: IJSONAPIResource<IRule>) => row.attributes?.invert },
  { name: 'match_type', align: 'center', label: 'Match Type', field: (row: IJSONAPIResource<IRule>) => row.attributes?.match_type },
  { name: 'key', align: 'center', label: 'Key', field: (row: IJSONAPIResource<IRule>) => row.attributes?.key },
  { name: 'pattern', align: 'center', label: 'Pattern', field: (row: IJSONAPIResource<IRule>) => row.attributes?.pattern }
];

const match_pagination = {
  rowsPerPage: 20,
  sortBy: "created_at",
  descending: true
}

const match_types = [
  {
    label: "Body",
    value: "BodyRule",
    keyed: false
  },
  {
    label: "Domain Name",
    value: "DomainNameRule",
    keyed: false
  },
  {
    label: "Endpoint",
    value: "EndpointRule",
    keyed: false
  },
  {
    label: "Header Key Exists",
    value: "HeaderKeyRule",
    keyed: false
  },
  {
    label: "Any Header Value",
    value: "HeaderValueRule",
    keyed: false
  },
  {
    label: "Specific Header Value",
    value: "HeaderKeyValueRule",
    keyed: true
  },
  {
    label: "HTTP Method",
    value: "MethodRule",
    keyed: false
  },
  {
    label: "Destination Port",
    value: "PortRule",
    keyed: false
  },
  {
    label: "Protocol",
    value: "ProtocolRule",
    keyed: false
  },
  {
    label: "Query Parameter Key Exists",
    value: "QueryParamKeyRule",
    keyed: false
  },
  {
    label: "Any Query Parameter Value",
    value: "QueryParamValueRule",
    keyed: false
  },
  {
    label: "Specific Query Parameter Value",
    value: "QueryParamKeyValueRule",
    keyed: true
  },
]
const http_verbs = ["DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "TRACE"];
const protocols = ["http", "https"];
const dialog = ref(false);

onMounted(async () => {
  RuleRepository.getAllRules()
    .then(response => {
      rules.value = response;
    })
})

async function buildAndOrTreeOrder(matches: IMatch[] | undefined): Promise<IMatch[] | undefined> {
  // Build the tree
  // Return the matches from root to leaf, top->bottom, left->right
  return matches;
}

async function showMatches(rule: IJSONAPIResource<IRule>) {
  debugger
  /*
   * Need to build the AND/OR tree here so that they are shown in the correct order
   */
  matches.value = await buildAndOrTreeOrder(rule.attributes?.matches);
  dialog.value = true;
}

</script>

<template>
  <div class="q-px-lg q-py-md">
    <q-table flat bordered dense title="Rules" :rows="rules" :columns="rule_columns" row-key="id"
      v-model:pagination="rule_pagination">

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
          <q-th>Actions</q-th>
        </q-tr>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <span v-if="col.name == 'name'">{{ col.value }}</span>
            <span v-else-if="col.name === 'created_at'">{{ moment(col.value).format("MMM D, YYYY @ h:mm:ss a") }}</span>
            <span v-else>{{ col.value }}</span>
          </q-td>
          <q-td>
            <q-btn @click="showMatches(props.row)">Matches</q-btn>
            <q-btn color="negative" @click="showMatches(props.row)">Delete</q-btn>
          </q-td>
        </q-tr>
      </template>

    </q-table>
    <q-dialog v-model="dialog">
      <q-card style="width: 800px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6 text-teal">Rule matches</div>
        </q-card-section>

        <q-card-section class="q-pt-none text-teal">
          <q-table flat bordered dense title="Matches" :rows="matches" :columns="match_columns" row-key="id"
            v-model:pagination="match_pagination">

            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th>Conjunction</q-th>
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                  {{ col.label }}
                </q-th>
                <q-th>Actions</q-th>
              </q-tr>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props" v-show="props.row['match_type'] != 'RootRule'">
                <q-td>
                  <q-btn size="xs" v-show="matches?.indexOf(props.row) > 1"> + AND</q-btn>
                  <q-btn size="xs" v-show="matches?.indexOf(props.row) > 1"> + OR</q-btn>
                </q-td>
                <q-td>
                  <q-checkbox v-model="props.row.invert" />
                </q-td>
                <q-td>
                  <q-select v-model="props.row.match_type" :options="match_types" label="Match Type"></q-select>
                </q-td>
                <q-td>
                  <q-input v-model="props.row.key" label="Key" v-show="props.row.match_type.keyed"/>
                </q-td>
                <q-td>
                  <q-input v-show="props.row.match_type != 'MethodRule' && props.row.match_type != 'ProtocolRule'" v-model="props.row.pattern" label="Pattern" />
                  <q-select v-show="props.row.match_type == 'MethodRule'" v-model="props.row.pattern" label="Pattern" :options="http_verbs"></q-select>
                  <q-select v-show="props.row.match_type == 'ProtocolRule'" v-model="props.row.pattern" label="Pattern" :options="protocols"></q-select>
                </q-td>
                <q-td>
                  <q-btn color="negative" @click="showMatches(this)">Remove</q-btn>
                </q-td>
              </q-tr>
            </template>

            <template v-slot:bottom-row>
              <q-tr>
                <q-td>
                  <q-btn size="xs"> + AND</q-btn>
                  <q-btn size="xs"> + OR</q-btn>
                </q-td>
                <q-td>
                  <q-btn color="positive" @click="showMatches(this)">Add</q-btn>
                </q-td>
              </q-tr>
            </template>
          </q-table>

        </q-card-section>

        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="OK" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>
