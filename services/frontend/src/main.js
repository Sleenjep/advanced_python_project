import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store"
import axios from "axios";

const app = createApp(App);

axios.defaults.withCredentials = true;

app.use(store);
app.use(router);
app.mount("#app");
