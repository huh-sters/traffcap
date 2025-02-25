<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import type { Ref } from 'vue';
import type { IRequest, IJSONAPIResource } from '@/types';
import { methodColors } from '@/maps';
import { ws_url } from '@/repositories/repository';
import { Notify, QTab } from 'quasar';
import type { QTableProps } from 'quasar';
import moment from 'moment';

const requests: Ref<IJSONAPIResource<IRequest>[]> = ref([]);
const columns = [
  { name: 'method', label: 'Method', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.method, sortable: true },
  { name: 'created_at', label: 'Created At', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.created_at, sortable: true },
  { name: 'endpoint_code', label: 'Endpoint Code', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.endpoint_code, sortable: true },
  { name: 'source_host', label: 'Source Host', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.source_host, sortable: true },
  { name: 'source_port', label: 'Source Port', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.source_port, sortable: true }
];
const pagination = ref({
  rowsPerPage: 10,
  sortBy: "created_at",
  descending: true,
  rowsNumber: 100,
  page: 1
});
let connection: WebSocket | undefined;

onMounted(async () => {
  connection = new WebSocket(`${ws_url}/traffic/ws`,);
  connection.onmessage = async (event: MessageEvent) => {
    if (event.data !== 'ping') {
      debugger
      const payload = await JSON.parse(event.data)
      requests.value = payload.data;
      pagination.value.page = payload.included[0].attributes.page;
      pagination.value.rowsNumber = payload.included[0].attributes.count;
    }
  };
})

onUnmounted(async () => {
  connection?.close();
})

async function copyData(data: string) {
  try {
    await navigator.clipboard.writeText(data);
    Notify.create('Request line copied to clipboard');
  } catch ($e) {
    console.info('Cannot copy to clipboard');
  }
}

async function onRequest(props: Parameters<NonNullable<QTableProps['onRequest']>>[0]) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination
  console.log(`onRequest called for page: ${page}`);
  console.log(props);
  connection?.close();
  connection = new WebSocket(`${ws_url}/traffic/ws/${page}/${rowsPerPage}`);
  connection.onmessage = async (event: MessageEvent) => {
    if (event.data !== 'ping') {
      debugger
      const payload = await JSON.parse(event.data)
      requests.value = payload.data;
      pagination.value.page = payload.included[0].attributes.page;
      pagination.value.rowsNumber = payload.included[0].attributes.count;
    }
  };
}
</script>

<template>
  <div class="q-px-lg q-py-md">
    <q-table flat bordered dense title="Requests" :rows="requests" :columns="columns" row-key="id"
      v-model:pagination="pagination" @request="onRequest">

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width></q-th>
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="xs" color="accent" round dense @click="props.expand = !props.expand"
              :icon="props.expand ? 'remove' : 'add'"></q-btn>
          </q-td>
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <span v-if="col.name == 'method'"><q-chip square text-color="white" :color="methodColors.get(col.value)">{{
                col.value }}</q-chip></span>
            <span v-else-if="col.name === 'created_at'">{{ moment(col.value).format("MMM D, YYYY @ h:mm:ss a") }}</span>
            <span v-else>{{ col.value }}</span>
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">
              <q-btn outline color="primary"
                @click="copyData(`${props.row.attributes.method} ${props.row.attributes.request_line} HTTP/1.1`)">{{
                  props.row.attributes.method }} {{ props.row.attributes.request_line }} HTTP/1.1</q-btn>
            </div>
          </q-td>
        </q-tr>
      </template>

      <template v-slot:pagination="scope">
        <q-btn v-if="scope.pagesNumber > 2" icon="first_page" color="grey-8" round dense flat
          :disable="scope.isFirstPage" @click="scope.firstPage" />

        <q-btn icon="chevron_left" color="grey-8" round dense flat :disable="scope.isFirstPage"
          @click="scope.prevPage" />

        <q-btn icon="chevron_right" color="grey-8" round dense flat :disable="scope.isLastPage"
          @click="scope.nextPage" />

        <q-btn v-if="scope.pagesNumber > 2" icon="last_page" color="grey-8" round dense flat :disable="scope.isLastPage"
          @click="scope.lastPage" />
      </template>
    </q-table>
  </div>
</template>
