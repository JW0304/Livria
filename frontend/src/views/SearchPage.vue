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
        :style="cardStyleMap[book.id] || {}"
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
import { ref, reactive, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import ColorThief from "colorthief";

const cardStyleMap = reactive({});

const route = useRoute();
const loading = ref(false);
const results = ref([]);

// 페이지네이션 상태 (임시 간단 구현)
const page = ref(1);
const perPage = 14;

function applyColorThiefToBooks(books) {
  for (let book of books) {
    const img = new Image();
    img.src = book.cover_url;
    img.crossOrigin = "anonymous";
    img.onload = () => {
      const thief = new ColorThief();
      const [r, g, b] = thief.getColor(img);
      const pal = thief.getPalette(img, 5);
      cardStyleMap[book.id] = {
        background: `linear-gradient(
          to bottom,
          rgb(${r},${g},${b}),
          rgb(${pal[1].join(",")})
        )`,
      };
    };
  }
}

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
    const res = await axios.get("/api/books/", {
      params: { search: q },
    });
    results.value = res.data.results || res.data;

    // ✅ 카드 배경 그라데이션 적용
    applyColorThiefToBooks(results.value);
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
  flex: 0 0 clamp(100px, 15vw, 180px);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 1.5rem;
  background: #222; /* 기본 배경 (추후 JS로 덮어씌울 수 있음) */
  text-decoration: none;
}
.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
}
.book-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
}
.book-title {
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgb(255, 255, 255);
  padding: 0 0.5rem;
}
.book-author {
  font-size: 0.75rem;
  color: rgb(221, 221, 221);
  margin: 0.25rem 0 0.5rem;
  padding: 0 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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
