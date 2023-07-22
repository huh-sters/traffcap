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
      />
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';


export default defineComponent({
  name: 'InboundRequests',
  mounted () {
    // Load the inbound requests
    // TODO: This needs to listen to a websocket
    axios
      .get(
        `http://localhost:9669/traffic`
      )
      .then((response) => {
        this.rows = response.data.data;
      })
  },
  data () {
    return {
      rows: [],
      columns: [
        { name: 'id', label: 'ID', align: 'left', field: (item) => {return item.id}, sortable: true },
        { name: 'endpoint_code', label: 'Endpoint Code', align: 'left', field: (item) => {return item.attributes.endpoint_code}, sortable: true },
        { name: 'method', label: 'Method', align: 'left', field: (item) => {return item.attributes.method}, sortable: true },
        { name: 'action', label: 'Action', align: 'left' }
      ]
    };
  }
});
</script>
