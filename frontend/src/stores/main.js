import { defineStore } from 'pinia'
import axios from 'axios'

export const useMainStore = defineStore('main', {
  state: () => ({
    bestSellers: [],
    ageRecs: [],
    topBooks: []
  }),
  actions: {
    async fetchBestSellers() {
      const { data } = await axios.get('/api/books/best-sellers')
      this.bestSellers = data
    },
    async fetchTopBooks() {
      const { data } = await axios.get('/api/books/top-recommended')
      this.topBooks = data
    },
    async fetchAgeBased(age = 20) {
      const { data } = await axios.get(`/api/books/age-based?age=${age}`)
      this.ageRecs = data
    }
  }
})
