<template>
  <div class="main-page">
    <section>
      <h2 @click="goToBestsellers" style="cursor: pointer">
        베스트 셀러
        <router-link to="/bestsellers" class="more-link">더보기</router-link>
      </h2>
      <div class="book-grid-wrapper">
        <button class="scroll-button left" @click="scrollLeft">‹</button>

        <div class="book-grid" ref="bookGrid">
          <div v-for="book in bestSellers" :key="book.id" class="book-card">
            <RouterLink :to="`/books/${book.id}`">
              <img :src="book.cover_url" alt="cover" />
              <h4>{{ book.title }}</h4>
              <p>{{ book.author_name }}</p>
            </RouterLink>
            <div class="menu-trigger" @click.stop.prevent="toggleMenu(book.id)">
              ⋯
            </div>
            <div v-if="openMenuId === book.id" class="context-menu">
              <button @click="playBook(book)">▷ 재생</button>
              <button @click="likeBook(book)">♡ 좋아요</button>
              <button @click="saveBook(book)">📁 찜하기</button>
            </div>
          </div>
        </div>

        <button class="scroll-button right" @click="scrollRight">›</button>
      </div>
    </section>

    <!-- <section v-if="isLoggedIn">
      <h2>오늘의 아리아</h2>
      <BookList :books="mainStore.ageRecs" />
    </section> -->

    <section>
      <h2>
        새로 도착한 도서
        <router-link to="/newbook" class="more-link">더보기</router-link>
      </h2>
      <div class="book-grid">
        <RouterLink
          v-for="book in newBooks"
          :key="book.id"
          :to="`/books/${book.id}`"
          class="book-card"
        >
          <img :src="book.cover_url" alt="cover" />
          <h4>{{ book.title }}</h4>
          <p>{{ book.author_name }}</p>
        </RouterLink>
      </div>
    </section>

    <section>
      <h2>
        블로거 추천 도서
        <router-link to="/recommendations" class="more-link"
          >더보기</router-link
        >
      </h2>
      <div class="book-grid">
        <RouterLink
          v-for="book in recommendedBooks"
          :key="book.id"
          :to="`/books/${book.id}`"
          class="book-card"
        >
          <img :src="book.cover_url" alt="cover" />
          <h4>{{ book.title }}</h4>
          <p>{{ book.author_name }}</p>
        </RouterLink>
      </div>
    </section>

    <!-- <section>
      <h2>많이 선호한 음악 추천</h2>
      <BookList :books="mainStore.topBooks" />
    </section> -->
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import axios from "axios";

import { useMainStore } from "@/stores/main";
import BookList from "@/components/BookList.vue";

import { useRouter } from "vue-router";
const router = useRouter();

const mainStore = useMainStore();
const isLoggedIn = computed(() => !!localStorage.token);

const bestSellers = ref([]);
const newBooks = ref([]);
const recommendedBooks = ref([]);

function handleScroll() {
  const el = bookGrid.value;
  if (!el) return;

  const nearEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - 50;
  if (nearEnd && bestSellers.value.length < 50) {
    loadMoreBooks(); // 조건은 적절히 조절
  }
}

function loadMoreBooks() {
  // 예: 새 책 5개 추가 (데모용)
  const moreBooks = bestSellers.value.slice(0, 5).map((b, i) => ({
    ...b,
    id: b.id + "_copy" + i, // 중복 방지용 ID
  }));
  bestSellers.value.push(...moreBooks);
}

onMounted(async () => {
  try {
    const bestsellerRes = await axios.get("/api/books/?category=1");
    bestSellers.value = bestsellerRes.data.slice(0, 15); // 상위 3개

    const newBookRes = await axios.get("/api/books/?category=2");
    newBooks.value = newBookRes.data.slice(0, 15); // 신간도 상위 3개 (원하면 더)

    const recommendationsRes = await axios.get("/api/books/?category=3");
    recommendedBooks.value = recommendationsRes.data.slice(0, 15);
  } catch (err) {
    console.error("도서 데이터 불러오기 실패:", err);

    bookGrid.value.addEventListener("scroll", handleScroll);
  }
});

function goToBestsellers() {
  router.push({ name: "BestSellers" }); // index.js에 이미 name으로 등록돼 있음
}

onMounted(async () => {
  await Promise.all([mainStore.fetchBestSellers(), mainStore.fetchTopBooks()]);

  if (!isLoggedIn.value) {
    await mainStore.fetchAgeBased(20); // 예시: 20대 추천 도서
  }
});

const openMenuId = ref(null);
function toggleMenu(id) {
  openMenuId.value = openMenuId.value === id ? null : id;
}
function playBook(book) {
  console.log("재생:", book);
}
function likeBook(book) {
  console.log("좋아요:", book);
}
function saveBook(book) {
  console.log("찜하기:", book);
}

const bookGrid = ref(null);

function scrollLeft() {
  bookGrid.value.scrollBy({ left: -800, behavior: "smooth" });
}
function scrollRight() {
  bookGrid.value.scrollBy({ left: 800, behavior: "smooth" });
}
</script>

<style scoped>
/* .book-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  justify-items: center;
  justify-content: center;
  max-width: 900px;
  margin: 0 auto; 
} */
.book-grid-wrapper {
  position: relative;
  overflow: hidden;
}

.book-grid {
  display: flex;
  gap: 0.5rem;
  overflow-x: hidden; /* ✅ 스크롤 막기 */
  scroll-behavior: smooth;
  padding: 0.5rem 0;
}

/* 좌우 버튼 */
.scroll-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  color: white;
  font-size: 1.5rem;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  border-radius: 4px;
}
.scroll-button.left {
  left: 0;
}
.scroll-button.right {
  right: 0;
}

.book-card img {
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
}

.book-card {
  flex: 0 0 auto;
  width: clamp(100px, 15vw, 180px); /* 반응형 너비 */
  background: black;
  border-radius: 10px;
  padding: 0.5rem;
  text-align: center;
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;

}
.book-card:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
}
.book-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.05),
    rgba(0, 0, 0, 0.3)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 10px;
  pointer-events: none;
}
.book-card:hover::after {
  opacity: 1;
}

.book-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}

.book-card h4 {
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: white; /* 제목 흰색 */
  text-decoration: none;
}

.book-card p {
  font-size: 0.75rem;
  color: gray;
  margin-top: 0.25rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
}
/* 스크롤 힌트용 오른쪽 화살표 버튼 */
/* .book-grid::after {
  content: "❯";
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 0.2rem 0.5rem;
  font-size: 1.2rem;
  border-radius: 4px;
  pointer-events: none;
} */

.book-card:hover {
  background-color: #0f0f0f;
  transform: scale(1.02);
  transition: all 0.24s;
}

.main-page {
  padding: 2rem;
  color: white;
}
section {
  margin-bottom: 3rem;
}
h2 {
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between; /* 제목과 더보기 링크를 양쪽으로 정렬 */
  align-items: center;
}

.more-link {
  font-size: 0.9rem;
  color: #aaa;
  cursor: pointer;
  text-decoration: none; /* 더보기 링크 밑줄 제거 */
}
</style>
