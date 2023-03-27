import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      path: "/signin",
      name: "signin",
      component: () => import("@/views/SigninView.vue"),
    },
    {
      path: "/emailsignin",
      name: "emailsignin",
      component: () => import("@/views/EmailSignInView.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/RegisterView.vue"),
    },
    {
      path: "/verifyemail",
      name: "verifyemail",
      component: () => import("@/views/VerifyEmailView.vue"),
    },
    {
      path: "/resetpassword",
      name: "resetpassword",
      component: () => import("@/views/ResetPasswordView.vue"),
    },
    {
      path: "/myaccount",
      name: "myaccount",
      component: () => import("@/views/MyAccountView.vue"),
    },
    {
      path: "/myreadinglist",
      name: "myreadinglist",
      component: () => import("@/views/MyReadingListView.vue"),
    },
    {
      path: "/search",
      name: "search",
      component: () => import("@/views/SearchView.vue"),
    },
    {
      path: "/ticker",
      name: "ticker",
      component: () => import("@/views/TickerView.vue"),
    },
    {
      path: "/category",
      name: "category",
      component: () => import("@/views/CategoryView.vue"),
    },
    {
      path: "/termsandconditions",
      name: "termsandconditions",
      component: () => import("@/views/TermsAndConditionsView.vue"),
    },
  ],
});

export default router;
