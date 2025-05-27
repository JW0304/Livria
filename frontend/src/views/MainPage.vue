<template>
  <div class="main-page">
    <!-- 베스트 셀러 섹션 -->
    <section>
      <h2 @click="goToBestsellers" style="cursor: pointer">
        베스트 셀러
        <router-link to="/bestsellers" class="more-link">더보기</router-link>
      </h2>
      <div class="grid-container">
        <button class="scroll-button left" @click="scrollLeft(bestGrid)">
          ‹
        </button>
        <div class="book-grid-wrapper">
          <div class="book-grid" ref="bestGrid">
            <div
              v-for="book in bestSellers"
              :key="book.id"
              class="book-card"
              :style="getCardStyle(book)"
            >
              <router-link :to="`/books/${book.id}`" class="card-link">
                <img :src="book.cover_url" alt="cover" />
                <h4>{{ book.title }}</h4>
                <p>{{ book.author_name }}</p>
              </router-link>
            </div>
          </div>
        </div>
        <button class="scroll-button right" @click="scrollRight(bestGrid)">
          ›
        </button>
      </div>
    </section>

    <!-- 새로 도착한 도서 섹션 -->
    <section>
      <h2>
        새로 도착한 도서
        <router-link to="/newbook" class="more-link">더보기</router-link>
      </h2>
      <div class="grid-container">
        <button class="scroll-button left" @click="scrollLeft(newGrid)">
          ‹
        </button>
        <div class="book-grid-wrapper">
          <div class="book-grid" ref="newGrid">
            <div
              v-for="book in newBooks"
              :key="book.id"
              class="book-card"
              :style="getCardStyle(book)"
            >
              <router-link :to="`/books/${book.id}`" class="card-link">
                <img :src="book.cover_url" alt="cover" />
                <h4>{{ book.title }}</h4>
                <p>{{ book.author_name }}</p>
              </router-link>
            </div>
          </div>
        </div>
        <button class="scroll-button right" @click="scrollRight(newGrid)">
          ›
        </button>
      </div>
    </section>

    <!-- 블로거 추천 도서 섹션 -->
    <section>
      <h2>
        블로거 추천 도서
        <router-link to="/recommendations" class="more-link"
          >더보기</router-link
        >
      </h2>
      <div class="grid-container">
        <button class="scroll-button left" @click="scrollLeft(recGrid)">
          ‹
        </button>
        <div class="book-grid-wrapper">
          <div class="book-grid" ref="recGrid">
            <div
              v-for="book in recommendedBooks"
              :key="book.id"
              class="book-card"
              :style="getCardStyle(book)"
            >
              <router-link :to="`/books/${book.id}`" class="card-link">
                <img :src="book.cover_url" alt="cover" />
                <h4>{{ book.title }}</h4>
                <p>{{ book.author_name }}</p>
              </router-link>
            </div>
          </div>
        </div>
        <button class="scroll-button right" @click="scrollRight(recGrid)">
          ›
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import ColorThief from "colorthief";
import { useMainStore } from "@/stores/main";

const bestSellers = ref([]);
const newBooks = ref([]);
const recommendedBooks = ref([]);

const bestGrid = ref(null);
const newGrid = ref(null);
const recGrid = ref(null);

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
      const [r, g, b] = thief.getColor(img);
      const pal = thief.getPalette(img, 5);
      resolve({
        background: `linear-gradient(to bottom, rgb(${r},${g},${b}), rgb(${pal[1].join(
          ","
        )}))`,
      });
    };
  });
};

function scrollLeft(gridRef) {
  const el = gridRef.value;
  if (!el) return;
  const card = el.querySelector(".book-card");
  const gap = parseFloat(getComputedStyle(el).gap) || 0;
  el.scrollTo({
    left: el.scrollLeft - (card.offsetWidth + gap),
    behavior: "smooth",
  });
}

function scrollRight(gridRef) {
  const el = gridRef.value;
  if (!el) return;
  const card = el.querySelector(".book-card");
  const gap = parseFloat(getComputedStyle(el).gap) || 0;
  el.scrollTo({
    left: el.scrollLeft + (card.offsetWidth + gap),
    behavior: "smooth",
  });
}

onMounted(async () => {
  const [bRes, nRes, rRes] = await Promise.all([
    axios.get("/api/books/?category=1"),
    axios.get("/api/books/?category=2"),
    axios.get("/api/books/?category=3"),
  ]);
  bestSellers.value = bRes.data.slice(0, 15);
  newBooks.value = nRes.data.slice(0, 15);
  recommendedBooks.value = rRes.data.slice(0, 15);

  await mainStore.fetchBestSellers();
  if (!isLoggedIn.value) {
    await mainStore.fetchAgeBased(20);
  }
});

function goToBestsellers() {
  router.push({ name: "BestSellers" });
}
</script>

<style scoped>
.main-page {
  padding: 2rem;
  background: transparent;
  color: white;
}

/* 바깥 컨테이너: 버튼 보이도록 overflow visible */
.grid-container {
  position: relative;
  width: calc((clamp(100px, 15vw, 180px) * 7) + (0.5rem * 6));
  margin: 0 auto 2rem;
  overflow: visible;
}

/* 내부 래퍼: 실제 클리핑은 여기서 */
.book-grid-wrapper {
  overflow: hidden;
}

/* 그리드: flex + x축 스크롤 */
.book-grid {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0.5rem 0;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.book-grid::-webkit-scrollbar {
  display: none;
}

/* 카드 크기 유지 */
.book-card {
  flex: 0 0 clamp(100px, 15vw, 180px);
  background: black;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-link {
  display: block;
  color: inherit;
  text-decoration: none;
}

.book-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.book-card h4 {
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: white;
  padding: 0 0.5rem;
}

.book-card p {
  font-size: 0.75rem;
  color: gray;
  margin: 0.25rem 0 0.5rem;
  padding: 0 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 버튼을 grid-container 바깥으로 배치 */
.scroll-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 2rem;
  height: 2rem;
  cursor: pointer;
  border-radius: 4px;
}
.scroll-button.left {
  left: -1.5rem;
}
.scroll-button.right {
  right: -1.5rem;
}

section h2 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.more-link {
  font-size: 0.9rem;
  color: #aaa;
  text-decoration: none;
}
</style>
