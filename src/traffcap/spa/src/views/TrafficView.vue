<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { Ref } from 'vue';
import type { IRequest, IJSONAPIResource } from '@/types';
import { methodIcons, methodColors } from '@/maps';
import { ws_url } from '@/repositories/repository';
import { TrafficRepository } from '@/repositories/traffic';

const requests: Ref<IJSONAPIResource<IRequest>[]> = ref([]);
const columns = [
  { name: 'method', label: 'Method', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.method },
  { name: 'request', label: 'Request', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.request_line },
  { name: 'created_at', label: 'Created At', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.created_at },
  { name: 'endpoint_code', label: 'Endpoint Code', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.endpoint_code },
  { name: 'source_host', label: 'Source Host', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.source_host },
  { name: 'source_port', label: 'Source Port', field: (row: IJSONAPIResource<IRequest>) => row.attributes?.source_port }
];
const pagination = {
  rowsPerPage: 20,
  sortBy: "created_at",
  descending: true
}
let connection: WebSocket | undefined;

onMounted(async () => {
  connection = new WebSocket(`${ws_url}/traffic/ws`,);
  connection.onmessage = async (event: MessageEvent) => {
    if (event.data !== 'ping') {
      requests.value = await JSON.parse(event.data).data;
    }
  };
  connection.onopen = async () => {
  };
  connection.onclose = async () => {
  };
  await TrafficRepository.getAllTraffic()
    .then(response => {
      requests.value = response;
    })
})

</script>

<template>
  <div class="q-px-lg q-py-md">
    <q-table flat bordered title="Treats" :rows="requests" :columns="columns" row-key="name" :pagination.sync="pagination">

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="sm" color="accent" round dense @click="props.expand = !props.expand"
              :icon="props.expand ? 'remove' : 'add'" />
          </q-td>
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">This is expand slot for row above: {{ props.row.name }}.</div>
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>
</template>
