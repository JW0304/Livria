<template>
  <div class="best-sellers-page">
    <h1>📚 베스트셀러 목록</h1>
    <div
      v-for="book in books"
      :key="book.id"
      class="book-card"
      @click="goToDetail(book.id)"
    >
      <img :src="book.image" alt="책 이미지" class="book-image" />

      <div class="book-info">
        <h2 class="book-title">{{ book.title }}</h2>
        <p class="book-author">작가: {{ book.author }}</p>
        <p class="book-pub">
          출판사: {{ book.publisher }}<br />출판일: {{ book.date }}
        </p>

        <div class="tags">
          <span v-for="tag in book.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <div class="audio-controls">
          <button class="play-btn">▶</button>
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
          <button class="download-btn">⬇</button>
        </div>

        <div class="icons">
          <span class="icon">♡</span>
          <span class="icon">👜</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

import { useRouter } from "vue-router";
const router = useRouter();

const books = ref([]);

function goToDetail(bookId) {
  router.push(`/books/${bookId}`);
}

onMounted(async () => {
  try {
    const res = await axios.get("http://localhost:8000/api/categories/3/");
    books.value = res.data.map((book) => ({
      id: book.id,
      title: book.title,
      author: book.author_name || "작자 미상",
      publisher: book.category_name || "출판사 미상",
      date: book.pub_date || "출판일 미상",
      image: book.cover_url || "/assets/default-cover.jpg",
      tags: ["소설/시/희곡", "사랑과 그리움", "에너자이저 그로우"], // 임시 태그, 나중에 AI 추출로 대체 가능
    }));
  } catch (err) {
    console.error("베스트셀러 데이터 불러오기 실패:", err);
  }
});
</script>

<style scoped>
.best-sellers-page {
  padding: 2rem;
  background: black;
  color: white;
}
.book-card {
  display: flex;
  gap: 1.5rem;
  padding: 1rem;
  margin-bottom: 2rem;
  border: 1px solid #aaa;
  border-radius: 8px;
}
.book-image {
  width: 160px;
  height: 220px;
  object-fit: cover;
  border-radius: 4px;
  background: #999;
}
.book-info {
  flex: 1;
}
.book-title {
  font-size: 1.8rem;
  margin-bottom: 0.3rem;
}
.book-author,
.book-pub {
  font-size: 1rem;
  margin: 0.2rem 0;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0.5rem 0;
}
.tag {
  background: #333;
  border: 1px solid #888;
  padding: 0.3rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}
.audio-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.8rem 0;
}
.play-btn,
.download-btn {
  background: transparent;
  color: white;
  font-size: 1.2rem;
  border: none;
  cursor: pointer;
}
.progress-bar {
  flex: 1;
  height: 6px;
  background: #444;
  border-radius: 3px;
  position: relative;
}
.progress-fill {
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, violet, purple);
  border-radius: 3px;
}
.icons {
  display: flex;
  gap: 1rem;
  font-size: 1.2rem;
  margin-top: 0.5rem;
}
</style>
