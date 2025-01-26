import { createRouter, createWebHistory } from 'vue-router'
import TrafficView from '@/views/TrafficView.vue'
import RulesView from '@/views/RulesView.vue'
import AboutView from '@/views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'traffic',
      component: TrafficView
    },
    {
      path: '/rules',
      name: 'rules',
      component: RulesView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    }
  ]
})

export default router
