// ✅ 1. stores/auth.js: 로그인, 회원가입, 토큰 처리
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
    error: ''
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Token ${token}`
    },
    async login(credentials) {
      try {
        const { data } = await axios.post('/api/auth/login', credentials)
        this.setToken(data.token)
        this.error = ''
      } catch (err) {
        this.error = '로그인에 실패했습니다.'
        throw err
      }
    },
    async signup(payload) {
      const { data } = await axios.post('/api/auth/signup', payload)
      this.setToken(data.token)
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})