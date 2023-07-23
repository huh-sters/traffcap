<template>
<q-toolbar>
    <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
    <q-toolbar-title>
      <q-img src="~assets/images/traffcap_logo.png" width="200px" />
    </q-toolbar-title>
  </q-toolbar>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
  
export default defineComponent({
  name: 'ToolBar',
  methods: {
    toggleLeftDrawer () {
      this.$emit('drawer-event');
    }
  }
});
</script>
