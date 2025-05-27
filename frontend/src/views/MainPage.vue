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
          <div
            v-for="book in bestSellers"
            :key="book.id"
            class="book-card"
            :style="getCardStyle(book)"
          >
            <RouterLink :to="`/books/${book.id}`">
              <img :src="book.cover_url" alt="cover" ref="cardImage" />
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
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import axios from "axios";
import { useMainStore } from "@/stores/main";
import { useRouter } from "vue-router";
import ColorThief from "colorthief";

const bestSellers = ref([]);
const newBooks = ref([]);
const recommendedBooks = ref([]);
const openMenuId = ref(null);
const bookGrid = ref(null);

const router = useRouter();
const mainStore = useMainStore();
const isLoggedIn = computed(() => !!localStorage.token);

const getCardStyle = (book) => {
  const img = new Image();
  img.src = book.cover_url;
  img.crossOrigin = "anonymous";
  return new Promise((resolve) => {
    img.onload = () => {
      const thief = new ColorThief();
      const dom = thief.getColor(img);
      const pal = thief.getPalette(img, 5);
      resolve({
        background: `linear-gradient(to bottom, rgb(${dom.join(
          ","
        )}), rgb(${pal[1].join(",")}))`,
      });
    };
  });
};

function handleScroll() {
  const el = bookGrid.value;
  if (!el) return;
  const nearEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - 50;
  if (nearEnd && bestSellers.value.length < 50) loadMoreBooks();
}

function loadMoreBooks() {
  const more = bestSellers.value.slice(0, 5).map((b, i) => ({
    ...b,
    id: b.id + "_copy" + i,
  }));
  bestSellers.value.push(...more);
}

onMounted(async () => {
  try {
    const res1 = await axios.get("/api/books/?category=1");
    bestSellers.value = res1.data.slice(0, 15);
    const res2 = await axios.get("/api/books/?category=2");
    newBooks.value = res2.data.slice(0, 15);
    const res3 = await axios.get("/api/books/?category=3");
    recommendedBooks.value = res3.data.slice(0, 15);
  } catch (e) {
    console.error(e);
  }
  bookGrid.value.addEventListener("scroll", handleScroll);

  await Promise.all([mainStore.fetchBestSellers(), mainStore.fetchTopBooks()]);
  if (!isLoggedIn.value) await mainStore.fetchAgeBased(20);
});

function goToBestsellers() {
  router.push({ name: "BestSellers" });
}
function toggleMenu(id) {
  openMenuId.value = openMenuId.value === id ? null : id;
}
function playBook(b) {
  console.log("재생:", b);
}
function likeBook(b) {
  console.log("좋아요:", b);
}
function saveBook(b) {
  console.log("찜하기:", b);
}
function scrollLeft() {
  bookGrid.value.scrollBy({ left: -800, behavior: "smooth" });
}
function scrollRight() {
  bookGrid.value.scrollBy({ left: 800, behavior: "smooth" });
}
</script>

<style scoped>
.main-page {
  padding: 2rem;
  color: white;
  background: transparent; /* 이제 body 배경이 보입니다 */
}

.book-grid-wrapper {
  position: relative;
  overflow: hidden;
}

.book-grid {
  display: flex;
  gap: 0.5rem;
  overflow-x: hidden;
  scroll-behavior: smooth;
  padding: 0.5rem 0;
}

/* 카드 크기를 키워서 한 줄에 보이는 수를 줄임 */
.book-card {
  flex: 0 0 auto;
  width: clamp(150px, 20vw, 200px);
  background: black;
  border-radius: 10px;
  padding: 0.5rem;
  text-align: center;
  color: inherit;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

/* 이하 기존 스타일 그대로 유지 */
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
  color: white;
}
.book-card p {
  font-size: 0.75rem;
  color: gray;
  margin-top: 0.25rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

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

section {
  margin-bottom: 3rem;
}
h2 {
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.more-link {
  font-size: 0.9rem;
  color: #aaa;
  text-decoration: none;
}
</style>
