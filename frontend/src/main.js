// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// ✅ Pinia 적용된 후에 authStore 호출
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
authStore.init()

// ✅ 기본 axios 전역 설정 (선택 사항, 기본 인스턴스 계속 쓸 거면 유지해도 됨)
axios.defaults.baseURL = 'http://localhost:8000/'

app.mount('#app')
