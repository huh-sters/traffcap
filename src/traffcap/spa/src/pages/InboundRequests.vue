<template>
  <q-page>
    <div class="q-pa-md">
      <q-banner v-if="notConnected" class="bg-red text-white">
        <q-icon name="error" /> {{ connectionError }}
        <template v-slot:action>
          <q-btn flat color="white" label="Retry" @click="openWebsocket()"/>
        </template>
      </q-banner>
      <q-card class="col-12" v-for="row in rows" :key="row.id">
        <q-card-section class="col-12">
          <q-chip square :color="method_colors[row.attributes.method]" text-color="white">{{ row.attributes.method }}</q-chip>
          Endpoint Code: {{ row.attributes.endpoint_code }}
          <q-btn>Copy</q-btn>
          <q-btn>Copy curl Request</q-btn>
        </q-card-section>
        <q-card-section class="col-6">
          <q-item-label>Query Params</q-item-label>
          <q-list dense>
            <q-item v-for="value, key in JSON.parse(row.attributes.query_params)" :key="key">{{ key }}: {{ value }}</q-item>
          </q-list>
        </q-card-section>
        <q-card-section class="col-6">
          <q-item-label>Headers</q-item-label>
          <q-list dense>
            <q-item v-for="value, key in JSON.parse(row.attributes.headers)" :key="key">{{ key }}: {{ value }}</q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Request } from 'components/models';
import { serverWebSocketURL } from 'components/server';
// import { JsonViewer } from 'vue3-json-viewer';


export default defineComponent({
  name: 'InboundRequests',
  components: {
    // JsonViewer
  },
  mounted () {
    // Load the inbound requests
    this.openWebsocket();
  },
  data () {
    return {
      connection: null as WebSocket | null,
      notConnected: false as boolean,
      connectionError: '' as string,
      method_colors: {
        GET: 'light-blue',
        POST: 'green',
        PATCH: 'cyan',
        PUT: 'orange',
        DELETE: 'red',
        TRACE: 'black',
        HEAD: 'deep-purple',
        OPTIONS: 'indigo'
      } as { [key: string]: string },
      rows: [] as Request[],
      columns: [
        { name: 'id', label: 'ID', align: 'left', field: (item: Request) => {return item.id}, sortable: true },
        { name: 'method', label: 'Method', align: 'left', field: (item: Request) => {return item.attributes.method}, sortable: true },
        { name: 'endpoint_code', label: 'Endpoint Code', align: 'left', field: (item: Request) => {return item.attributes.endpoint_code}, sortable: true },
        { name: 'action', label: 'Action', align: 'left' }
      ]
    };
  },
  methods: {
    chipColor(method: string) {
      return method_colors[method];
    },
    openWebsocket() {
      this.connection = new WebSocket(`${serverWebSocketURL()}/traffic/ws`);
      this.connection.onmessage = (event: MessageEvent) => {
        this.rows = JSON.parse(event.data).data;
      }
      this.connection.onopen = () => {
        this.notConnected = false;
      }
      this.connection.onclose = () => {
        this.notConnected = true;
        this.connectionError = 'Cannot connect to the Traffcap server';
      }
    }
  }
});
</script>
