import { createApp } from "vue";
import { createPinia } from "pinia";
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css'

import App from './App.vue' ;
import router from "./router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

const app = createApp(App);

app.use(createPinia());
app.use(router);

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCircleExclamation,
  faHome,
  faMagnifyingGlass,
  faUser,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
library.add(faCircleExclamation, faHome, faMagnifyingGlass, faUser, faUserPlus);

app.use(Antd).mount("#app");
