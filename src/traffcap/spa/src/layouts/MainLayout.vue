<template>
  <q-layout view="hHh lpR fFf">
    <q-header bordered class="bg-primary text-white">
      <ToolBar @drawer-event="toggleDrawer" />
    </q-header>
    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <LeftMenu />
    </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import LeftMenu from 'src/components/LeftMenu.vue'
import ToolBar from 'src/components/Toolbar.vue'

export default {
  components: {
    LeftMenu,
    ToolBar
  },
  data () {
    return {
      leftDrawerOpen: true
    }
  },
  methods: {
    toggleDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen
    }
  }
}
</script>