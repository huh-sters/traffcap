<template>
  <q-page>
    <div class="q-pa-md">
      <q-table
        flat bordered
        title="Inbound Requests"
        dense
        :rows="rows"
        :columns="columns"
        row-key="name"
        :rows-per-page-options="[0]"
      >
        <template v-slot:body-cell-method="props">
          <q-chip color="light-blue" text-color="white">{{ props.row.attributes.method }}</q-chip>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';


type Request = {
  id: string,
  type: string,
  attributes: {
    endpoint_code: string,
    method: string,
    headers: string,
    query_params: string,
    body: string,
    id: number
  }
}

export default defineComponent({
  name: 'InboundRequests',
  mounted () {
    // Load the inbound requests
    this.connection = new WebSocket('ws://localhost:9669/traffic/ws');
    this.connection.onmessage = (event: MessageEvent) => {
      this.rows = JSON.parse(event.data).data;
    }
    this.connection.onopen = () => {
      console.log('Opened websocket...')
    }
  },
  data () {
    return {
      connection: null as WebSocket | null,
      rows: [] as Request[],
      columns: [
        { name: 'id', label: 'ID', align: 'left', field: (item: Request) => {return item.id}, sortable: true },
        { name: 'endpoint_code', label: 'Endpoint Code', align: 'left', field: (item: Request) => {return item.attributes.endpoint_code}, sortable: true },
        { name: 'method', label: 'Method', align: 'left', field: (item: Request) => {return item.attributes.method}, sortable: true },
        { name: 'action', label: 'Action', align: 'left' }
      ]
    };
  }
});
</script>
