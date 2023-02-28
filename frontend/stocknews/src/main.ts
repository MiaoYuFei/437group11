import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.config.globalProperties.$projectName = "Stock news";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCircleExclamation,
  faEnvelope,
  faHome,
  faMagnifyingGlass,
  faUser,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
library.add(
  faCircleExclamation,
  faEnvelope,
  faHome,
  faMagnifyingGlass,
  faUser,
  faUserPlus
);

app.mount("#app");
