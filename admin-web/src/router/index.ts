import { createRouter, createWebHistory } from 'vue-router'

import Layout from '../layout/Layout.vue'
import Login from '../views/Login.vue'
import Posts from '../views/Posts.vue'
import Users from '../views/Users.vue'
import Stats from '../views/Stats.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/',
      component: Layout,
      redirect: '/users',
      children: [
        {
          path: '/users',
          name: 'users',
          component: Users,
        },
        {
          path: '/posts',
          name: 'posts',
          component: Posts,
        },
        {
          path: '/stats',
          name: 'stats',
          component: Stats,
        },
      ],
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.name === 'login') {
    if (token) {
      next({ path: '/users' })
    } else {
      next()
    }
    return
  }

  if (!token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  next()
})

export default router
