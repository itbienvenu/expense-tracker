import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../pages/DashboardComponent.vue";
import Auth from "../components/AuthView.vue";


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "", component: Auth},
    { path: '/auth', component: Auth },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  ]
});

router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('accessToken');
  if (to.meta.requiresAuth && !accessToken) {
    next('/auth');
  } else if (to.path === '/auth' && accessToken) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
