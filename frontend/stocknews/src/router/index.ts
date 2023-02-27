import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import RegisterView from "@/views/RegisterView.vue";
import SigninView from "@/views/SigninView.vue";
import ProfileView from "@/views/ProfileView.vue";
import SearchView from "@/views/SearchView.vue";
import TickerView from "@/views/TickerView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/signin",
      name: "signin",
      component: SigninView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/search",
      name: "search",
      component: SearchView,
    },
    {
      path: "/ticker",
      name: "ticker",
      component: TickerView,
    },
  ],
});

export default router;
