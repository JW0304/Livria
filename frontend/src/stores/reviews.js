import { defineStore } from "pinia";
import axios from "axios";

// ✅ 5. stores/reviews.js: 감상 리뷰 목록 + 작성
export const useReviewStore = defineStore("reviews", {
  state: () => ({ list: [], total: 0, page: 1 }),
  actions: {
    async fetchReviews(bookId) {
      const { data } = await axios.get(`/api/reviews?book=${bookId}`);
      this.list = data;
    },
    async fetchAll(page = 1) {
      const res = await axios.get("/api/reviews", { params: { page } });
      this.list = res.data.results;
      this.total = res.data.count;
      this.page = page;
    },
    async postReview(payload) {
      await axios.post("/api/reviews", payload);
      await this.fetchReviews(payload.book);
    },
  },
});
