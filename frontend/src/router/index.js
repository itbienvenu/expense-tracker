import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../pages/DashboardComponent.vue";
import Auth from "../components/AuthView.vue";

const routes = [
  { path: "/", redirect: "/auth" },
  { path: "/auth", component: Auth },
  { path: "/dashboard", component: Dashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
