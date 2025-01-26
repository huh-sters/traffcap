<template>
  <q-header elevated class="bg-primary text-white">
    <q-toolbar class="bg-primary glossy text-white">
      <q-toolbar-title shrink>
        <img src="@/assets/traffcap_logo.png" height="40em">
      </q-toolbar-title>
      <q-tabs>
        <q-route-tab :to="{ name: 'traffic' }" name="traffic">Inbound Traffic</q-route-tab>
        <q-route-tab :to="{ name: 'rules' }" name="rules">Rules</q-route-tab>
        <q-route-tab :to="{ name: 'about' }" name="about">About</q-route-tab>
      </q-tabs>
    </q-toolbar>
  </q-header>
</template>

<script setup lang="ts">
</script>

<style scoped>
</style>