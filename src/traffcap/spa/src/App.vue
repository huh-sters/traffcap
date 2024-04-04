<script setup lang="ts">
import { RouterView } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue';

</script>

<template>
  <q-layout view="hHh LpR fFf">
    <PageHeader />

    <q-page-container>
      <RouterView />
    </q-page-container>

  </q-layout>
</template>

<style scoped>
</style>
