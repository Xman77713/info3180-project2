import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginFormView from '../views/LoginFormView.vue'
import RegisterFormView from '../views/RegisterFormView.vue'
import NewPostView from '../views/NewPostView.vue'
import LogoutView from '../views/LogoutView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/explore',
      name: 'explore',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/PostsView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginFormView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterFormView
    },
    {
      path: '/posts/new',
      name: 'newPosts',
      component: NewPostView
    },
    {
      path: '/users/:user_id',
      name: 'profile',
      component: () => import('../views/UserView.vue')
    }
  ]
})

export default router
