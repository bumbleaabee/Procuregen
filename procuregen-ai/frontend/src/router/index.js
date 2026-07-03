import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/generate', name: 'generate', component: () => import('../views/GenerateView.vue') },
  { path: '/history', name: 'history', component: () => import('../views/HistoryView.vue') },
  { path: '/templates', name: 'templates', component: () => import('../views/TemplateView.vue') },
  { path: '/chat', name: 'chat', component: () => import('../views/ChatView.vue') },
  { path: '/analytics', name: 'analytics', component: () => import('../views/AnalyticsView.vue') },
  { path: '/knowledge', name: 'knowledge', component: () => import('../views/KnowledgeView.vue') },
  { path: '/polish', name: 'polish', component: () => import('../views/PolishView.vue') },
  { path: '/guide', name: 'guide', component: () => import('../views/GuideView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
