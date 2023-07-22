import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/', component: () => import('pages/InboundRequests.vue') },
      { path: 'inbound_requests', component: () => import('pages/InboundRequests.vue') },
      { path: 'actions', component: () => import('pages/InboundRequests.vue') },
      { path: 'responses', component: () => import('pages/InboundRequests.vue') },
      { path: 'groups', component: () => import('pages/InboundRequests.vue') },
      { path: 'users', component: () => import('pages/InboundRequests.vue') },
      { path: 'logout', component: () => import('pages/InboundRequests.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
