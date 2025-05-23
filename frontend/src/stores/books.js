import { defineStore } from "pinia";
import axios from "axios";

// ✅ 2. stores/books.js: 도서 전체, 카테고리, 검색 결과
export const useBooksStore = defineStore("books", {
  state: () => ({ books: [], total: 0, page: 1 }),
  actions: {
    async fetchBooks(page = 1) {
      const res = await axios.get("/api/books/list", { params: { page } });
      this.books = res.data.books;
      this.total = res.data.total;
      this.page = page;
    },
    async fetchCategoryBooks(category, page = 1) {
      const res = await axios.get(`/api/books/category/${category}`, {
        params: { page },
      });
      this.books = res.data.books;
      this.total = res.data.total;
      this.page = page;
    },
    async searchBooks(query, page = 1) {
      const res = await axios.get("/api/books/search", {
        params: { q: query, page },
      });
      this.books = res.data.books;
      this.total = res.data.total;
      this.page = page;
    },
  },
});
