<template>
  <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
        <q-item clickable v-ripple>
          <q-item-section avatar>
          <q-avatar square>
            <img src="https://i.pravatar.cc/800" />
          </q-avatar>
        </q-item-section>
        <q-item-section>Incoming Requests</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar square>
            <img src="https://i.pravatar.cc/800" />
          </q-avatar>
        </q-item-section>
        <q-item-section>Actions</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar square>
            <img src="https://i.pravatar.cc/800" />
          </q-avatar>
        </q-item-section>
        <q-item-section>Registered Endpoints</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar square>
            <img src="https://i.pravatar.cc/800" />
          </q-avatar>
        </q-item-section>
        <q-item-section>Settings</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'LeftMenu',
  props: {},
  setup() {
    return {};
  },
});
</script>
