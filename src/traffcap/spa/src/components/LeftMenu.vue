<template>
  <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
      <q-item v-for="item in menuItems" clickable v-ripple :key="item.title" :to="item.path" :href="item.href">
        <q-item-section><q-icon :name="item.icon" size="xl"></q-icon></q-item-section>
        <q-item-section>{{ item.title }}</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LeftMenu',
  data() {
    return {
      menuItems: [
        { title: 'Inbound Requests', icon: 'history', path: '/inbound_requests' },
        { title: 'Actions', icon: 'bolt', path: '/actions' },
        { title: 'Responses', icon: 'reply', path: '/responses' },
        { title: 'Groups', icon: 'people', path: '/groups' },
        { title: 'OpenAPI Doc', icon: 'description', href: '/docs' },
        { title: 'Redoc', icon: 'description', href: '/redoc' },
        { title: 'Users', icon: 'person', path: '/users' },
        { title: 'Logout', icon: 'logout', path: '/logout' },
      ]
    }
  }
});
</script>
