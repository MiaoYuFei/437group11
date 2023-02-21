import { createRouter, createWebHistory } from "vue-router";
import HomeViewVue from "@/views/HomeView.vue";
import RegisterViewVue from "@/views/RegisterView.vue";
import LoginViewVue from "@/views/LoginView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeViewVue,
    },
    {
      path: "/login",
      name: "login",
      component: LoginViewVue,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterViewVue,
    },
  ],
});

export default router;
