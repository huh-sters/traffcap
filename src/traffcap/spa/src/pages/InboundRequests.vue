<template>
  <q-page>
    <div class="q-pa-md">
      <q-banner v-if="notConnected" class="bg-red text-white">
        <q-icon name="error" /> {{ connectionError }}
        <template v-slot:action>
          <q-btn flat color="white" label="Retry" @click="openWebsocket()"/>
        </template>
      </q-banner>
      <q-list padding bordered class="rounded-borders">
        <q-item v-for="row in rows" :key="row.id">
          <q-item-section>
            <q-item-label>
              <q-chip square :color="method_colors[row.attributes.method]" text-color="white">{{ row.attributes.method }} @ {{ row.attributes.endpoint_code }}</q-chip>
            </q-item-label>
          </q-item-section>
          <q-item-section>
            <q-item-label>Query Params</q-item-label>
            <JsonViewer :value="JSON.parse(row.attributes.query_params)" copyable boxed sort/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Headers</q-item-label>
            <JsonViewer :value="JSON.parse(row.attributes.headers)" copyable boxed sort/>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Request } from 'components/models';
import { serverWebSocketURL } from 'components/server';
import { JsonViewer } from 'vue3-json-viewer';


export default defineComponent({
  name: 'InboundRequests',
  components: {
    JsonViewer
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
