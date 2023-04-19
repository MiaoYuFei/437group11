import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
// @ts-ignore
import Vue3Tour from "vue3-tour";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

import "vue3-tour/dist/vue3-tour.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(Vue3Tour);

app.config.globalProperties.$projectName = "Stock news";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBars,
  faCircleExclamation,
  faEnvelope,
  faHome,
  faLink,
  faLock,
  faMagnifyingGlass,
  faPhone,
  faTableList,
  faUser,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
library.add(
  faBars,
  faCircleExclamation,
  faEnvelope,
  faHome,
  faLink,
  faLock,
  faMagnifyingGlass,
  faPhone,
  faTableList,
  faUser,
  faUserPlus
);

app.mount("#app");
