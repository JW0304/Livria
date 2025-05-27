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
        :style="cardStyleMap[book.id] || {}"
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
import { ref, computed, onMounted, watch, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import ColorThief from "colorthief";

const route = useRoute();
const router = useRouter();

const books = ref([]);
const allGenres = ref([]);
const totalBooks = ref(0);
const cardStyleMap = reactive({});

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

  // ✅ 여기에 추가!
  applyColorThiefToBooks(books.value);
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
  margin-top: 5rem;
  padding: 2rem;
  background: transparent;
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
  background: #333; /* 선택 안 됐을 때 진회색 */
  border: none;
  border-radius: 20px;
  padding: 0.3rem 0.8rem;
  cursor: pointer;
  font-weight: bold;
  color: #ccc; /* 연한 회색 글씨 */
  transition: all 0.2s ease;
}

/* 선택된 버튼 */
.genre-filter button.selected {
  background: linear-gradient(to right, #e718b4, #4cc2fe);
  color: white;
}

/* 선택된 버튼 호버 시 (더 밝은 그라데이션 + 확대) */
.genre-filter button.selected:hover {
  background: linear-gradient(to right, #ff42cc, #73d5ff);
  transform: scale(1.05);
}

/* 선택 안 된 버튼 호버 시 (약간 밝게 + 살짝 커짐) */
.genre-filter button:not(.selected):hover {
  background: #555;
  color: #eee;
  transform: scale(1.03);
}

.result-count {
  margin-top: 2rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: rgb(160, 160, 160);
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr); /* ✅ 7개 고정 */
  gap: 1rem;
  margin-bottom: 3rem;
}
.book-card {
  flex: 0 0 clamp(100px, 15vw, 180px);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 1.5rem;
  background: #222; /* 기본 배경 – JS에서 덮어씌움 */
  text-decoration: none;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
}
.book-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 6px;
}
.book-title {
  font-weight: ;
  color: white;
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-decoration: none;
}
.book-author {
  color: rgb(218, 217, 217);
  font-size: 0.8rem;
  margin: 0.5rem 0 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-decoration: none;

  /* ✅ 추가 스타일 */

  -webkit-text-stroke: 0.3px rgb(255, 255, 255);
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
  color: rgb(163, 163, 163);
  font-weight: bold;
  cursor: pointer;
}
.pagination button.current {
  color: #b31cb3;
  text-decoration: underline;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
