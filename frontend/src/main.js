import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

async function bootstrap() {
  const app = createApp(App);
  window.__app__ = app;

  // 1) 토큰 헤더 복구
  const token = localStorage.getItem("token");
  if (token) {
    axios.defaults.headers.common["Authorization"] = `Token ${token}`;
  }
  axios.defaults.baseURL = "http://localhost:8000/";

  // 2) Pinia & Router
  const pinia = createPinia();
  app.use(pinia);
  app.use(router);

  // 3) auth.init() 호출로 토큰·유저 복원
  const auth = useAuthStore();
  auth.init();

  // 4) 마운트
  app.mount("#app");
}

bootstrap();
