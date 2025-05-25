// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)
window.__app__ = app  // ✅ 이거만 추가하면 콘솔에서 Vue 인스턴스 접근 가능!

const pinia = createPinia()

app.use(pinia)
app.use(router)

// ✅ 1. 토큰 먼저 복구
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token}`
}

// ✅ 2. store 사용은 그 다음
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()

// ✅ 3. authStore 내부에서 user를 초기화하는 메서드가 필요하다면 여기서
authStore.init?.()  // ✅ 요 줄이 핵심이야!! fetchMe가 아니라 이걸 써야 user 복구됨

// ✅ 4. 기본 axios 설정 (선택)
axios.defaults.baseURL = 'http://localhost:8000/'

app.mount('#app')
