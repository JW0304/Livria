<template>
  <div class="search-page">
    <div class="filters">
      <!-- 검색 페이지에는 필터 UI 비활성화 상태 유지 -->
    </div>

    <section v-if="loading">불러오는 중...</section>
    <section v-else-if="!filteredBooks.length">검색 결과가 없습니다.</section>
    <section class="book-grid" v-else>
      <RouterLink
        v-for="book in filteredBooks"
        :key="book.id"
        :to="`/books/${book.id}`"
        class="book-card"
      >
        <img :src="book.cover_url" alt="book cover" />
        <p class="book-title">{{ book.title }}</p>
        <p class="book-author">{{ book.author_name }}</p>
      </RouterLink>
    </section>

    <div class="pagination">
      <button class="arrow" @click="prevPage" :disabled="page === 1">◀</button>
      <button class="arrow" @click="nextPage" :disabled="page === totalPages">
        ▶
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const loading = ref(false);
const results = ref([]);

// 페이지네이션 상태 (임시 간단 구현)
const page = ref(1);
const perPage = 12;

const filteredBooks = computed(() => {
  const start = (page.value - 1) * perPage;
  return results.value.slice(start, start + perPage);
});
const totalPages = computed(() => Math.ceil(results.value.length / perPage));

function prevPage() {
  if (page.value > 1) page.value--;
}
function nextPage() {
  if (page.value < totalPages.value) page.value++;
}

async function fetchSearchResults(q) {
  loading.value = true;
  try {
    // DRF SearchFilter: ?search=<query>
    const res = await axios.get("/api/books/", {
      params: { search: q },
    });
    // DRF pagination: res.data.results, non-paginated: res.data
    results.value = res.data.results || res.data;
  } catch (err) {
    console.error("검색 실패:", err);
    results.value = [];
  } finally {
    loading.value = false;
    page.value = 1;
  }
}

onMounted(() => {
  const q = route.query.q;
  if (q) fetchSearchResults(q);
});

watch(
  () => route.query.q,
  (newQ) => {
    if (newQ) fetchSearchResults(newQ);
    else results.value = [];
  }
);
</script>

<style scoped>
.search-page {
  padding: 2rem;
  background: transparent;
  color: white;
  min-height: 100vh;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1.5rem;
}
.book-card {
  background: rgb(0, 0, 0);
  color: rgb(255, 255, 255);
  padding: 0.5rem;
  border-radius: 8px;
  text-align: center;
}
.book-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
}
.book-title {
  font-weight: bold;
  margin: 0.5rem 0 0;
}
.book-author {
  margin: 0.2rem 0 0;
}
.pagination {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}
.arrow {
  background: #444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
}
.arrow:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
