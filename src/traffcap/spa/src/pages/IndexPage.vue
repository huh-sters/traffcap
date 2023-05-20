<template>
  <q-page class="row items-center justify-evenly">
    <RequestTimeline />
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import RequestTimeline from 'src/components/RequestTimeline.vue';

export default defineComponent({
  name: 'IndexPage',
  components: { RequestTimeline },
  setup () {
    return { };
  }
});
</script>
