// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import home from './home.js'
import NotFound from '@/views/NotFound.vue'
import admin from './admin.js'
import role from './role.js'
import permission from './permission.js'
import users from './users.js'
import food from './food.js'

const routes = [
  ...home,
  ...admin,
  ...role,
  ...permission,
  ...users,
  ...food,
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
