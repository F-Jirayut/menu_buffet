// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import home from './home.js'
import NotFound from '@/views/NotFound.vue'
import admin from './admin.js'

const routes = [
  ...home,
  ...admin,
  // ใส่ route not found ก็ได้
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
