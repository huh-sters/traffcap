<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { IRequest, IJSONAPIResource } from '@/types';
import { methodIcons, methodColors } from '@/maps';
import { ws_url } from '@/repositories/repository';
import { TrafficRepository } from '@/repositories/traffic';

const requests = ref<IJSONAPIResource<IRequest>[]>();

let connection: WebSocket | undefined;

onMounted(() => {
  connection = new WebSocket(`${ws_url}/traffic/ws`);
  connection.onmessage = (event: MessageEvent) => {
    if (event.data !== 'ping') {
      requests.value = JSON.parse(event.data).data as IJSONAPIResource<IRequest>[];
    }
  };
  connection.onopen = () => {
    console.log("Connected!");
  };
  connection.onclose = () => {
    console.log("Closed!");
  };
  TrafficRepository.getAllTraffic()
    .then(response => {
      
    })
})

</script>

<template>
  <div class="q-px-lg q-py-md">
    <q-timeline color="secondary" layout="dense" side="right">
      <q-timeline-entry
        v-for="request, index in requests"
        :key="index"
        :title="`${request.attributes.method}&nbsp;(${request.attributes.endpoint_code})`"
        :icon="methodIcons.get(request.attributes.method)"
        :color="methodColors.get(request.attributes.method)"
      >{{ request.attributes.body }}</q-timeline-entry>
    </q-timeline>
  </div>
</template>