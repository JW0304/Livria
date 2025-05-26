<template>
  <div class="genre-page">
    <!-- 장르 버튼 목록 -->
    <div class="genre-filter">
      <span>카테고리</span>
      <button
        :class="{
          selected: route.params.id === undefined || route.params.id === 'all',
        }"
        @click="changeGenre('all')"
      >
        전체
      </button>
      <button
        v-for="g in allGenres"
        :key="g.id"
        :class="{ selected: route.params.id === String(g.id) }"
        @click="changeGenre(String(g.id))"
      >
        {{ g.name }}
      </button>
    </div>

    <!-- 총 검색 결과 수 -->
    <p class="result-count">총 {{ totalBooks }} 권의 책이 검색되었습니다.</p>

    <!-- 도서 목록 -->
    <div class="book-grid">
      <RouterLink
        v-for="book in paginatedBooks"
        :key="book.id"
        :to="`/books/${book.id}`"
        class="book-card"
      >
        <img :src="book.cover_url" alt="book cover" />
        <p class="book-title">{{ book.title }}</p>
        <p class="book-author">{{ book.author_name }}</p>
      </RouterLink>
    </div>

    <!-- 페이지 네비게이션 -->
    <div class="pagination">
      <button @click="goToFirst" :disabled="page === 1">⏮</button>
      <button @click="prevPage" :disabled="page === 1">◀</button>

      <button
        v-for="p in totalPages"
        :key="p"
        :class="{ current: p === page }"
        @click="page = p"
      >
        {{ p }}
      </button>

      <button @click="nextPage" :disabled="page === totalPages">▶</button>
      <button @click="goToLast" :disabled="page === totalPages">⏭</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();

const books = ref([]);
const allGenres = ref([]);
const totalBooks = ref(0);

const page = ref(1);
const perPage = 12;

const paginatedBooks = computed(() => {
  const start = (page.value - 1) * perPage;
  return books.value.slice(start, start + perPage);
});
const totalPages = computed(() => Math.ceil(books.value.length / perPage));

function nextPage() {
  if (page.value < totalPages.value) page.value++;
}
function prevPage() {
  if (page.value > 1) page.value--;
}
function goToFirst() {
  page.value = 1;
}
function goToLast() {
  page.value = totalPages.value;
}

function changeGenre(id) {
  // 항상 /genre/<id> 형태로 이동
  router.push(id === "all" ? `/genre/all` : `/genre/${id}`);
}

async function fetchGenreBooks(genreId) {
  // 장르 목록은 공통으로 API에서 가져옴
  const { data: genres } = await axios.get("/api/genres/");
  allGenres.value = genres;

  if (!genreId || genreId === "all") {
    // 전체 도서
    const { data: allBooks } = await axios.get("/api/books/");
    books.value = allBooks;
  } else {
    // 특정 장르 도서
    const { data: genreBooks } = await axios.get(
      `/api/books/?genre=${genreId}`
    );
    books.value = genreBooks;
  }

  totalBooks.value = books.value.length;
  page.value = 1;
}

onMounted(() => {
  fetchGenreBooks(route.params.id);
});
watch(
  () => route.params.id,
  (id) => {
    fetchGenreBooks(id);
  }
);
</script>

<style scoped>
.genre-page {
  padding: 2rem;
  color: white;
  text-align: center;
}
.genre-filter {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
  color: lightgray;
}
.genre-filter button {
  background: #eee;
  border: none;
  border-radius: 20px;
  padding: 0.3rem 0.8rem;
  cursor: pointer;
}
.genre-filter button.selected {
  background: #a96acc;
  color: white;
}
.result-count {
  margin: 1rem 0;
  font-size: 0.9rem;
  color: gray;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.book-card {
  background: #111;
  padding: 1rem;
  border-radius: 0.5rem;
  text-decoration: none;
}
.book-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 6px;
}
.book-title,
.book-author {
  color: white;
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.3rem;
  flex-wrap: wrap;
}
.pagination button {
  background: none;
  border: none;
  padding: 0.4rem 0.6rem;
  color: white;
  font-weight: bold;
  cursor: pointer;
}
.pagination button.current {
  color: #a96acc;
  text-decoration: underline;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
