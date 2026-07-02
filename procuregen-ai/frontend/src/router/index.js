import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/generate', name: 'generate', component: () => import('../views/GenerateView.vue') },
  { path: '/history', name: 'history', component: () => import('../views/HistoryView.vue') },
  { path: '/templates', name: 'templates', component: () => import('../views/TemplateView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
