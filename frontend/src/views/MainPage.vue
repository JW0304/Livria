<template>
  <div class="main-page">
    <!-- 배너 슬라이더 -->
    <div class="banner-slider">
      <div
        class="banner-track"
        :style="{ transform: `translateX(-${currentBanner * 100}%)` }"
      >
        <div class="banner-slide" v-for="(src, i) in bannerImages" :key="i">
          <img :src="src" alt="banner" />
        </div>
      </div>
    </div>

    <!-- 베스트 셀러 섹션 -->
    <section>
      <h2 @click="goToBestsellers" class="section-title">
        베스트 셀러
        <router-link to="/bestsellers" class="more-link">더보기</router-link>
      </h2>
      <div class="slider-container">
        <button class="slide-btn left" @click="slidePrev('best')">‹</button>
        <div class="cards-wrapper">
          <div class="cards">
            <div
              v-for="book in bestSellers.slice(
                bestIndex,
                bestIndex + visibleCount
              )"
              :key="book.id"
              class="book-card"
              :style="cardStyleMap[book.id] || {}"
            >
              <router-link :to="`/books/${book.id}`" class="card-link">
                <img :src="book.cover_url" alt="cover" />
                <h4>{{ book.title }}</h4>
                <p>{{ book.author_name }}</p>
              </router-link>
            </div>
          </div>
        </div>
        <button class="slide-btn right" @click="slideNext('best')">›</button>
      </div>
    </section>

    <!-- 새로 도착한 도서 섹션 -->
    <section>
      <h2 class="section-title">
        새로 도착한 도서
        <router-link to="/newbook" class="more-link">더보기</router-link>
      </h2>
      <div class="slider-container">
        <button class="slide-btn left" @click="slidePrev('new')">‹</button>
        <div class="cards-wrapper">
          <div class="cards">
            <div
              v-for="book in newBooks.slice(newIndex, newIndex + visibleCount)"
              :key="book.id"
              class="book-card"
              :style="cardStyleMap[book.id] || {}"
            >
              <router-link :to="`/books/${book.id}`" class="card-link">
                <img :src="book.cover_url" alt="cover" />
                <h4>{{ book.title }}</h4>
                <p>{{ book.author_name }}</p>
              </router-link>
            </div>
          </div>
        </div>
        <button class="slide-btn right" @click="slideNext('new')">›</button>
      </div>
    </section>

    <!-- 블로거 추천 도서 섹션 -->
    <section>
      <h2 class="section-title">
        블로거 추천 도서
        <router-link to="/recommendations" class="more-link"
          >더보기</router-link
        >
      </h2>
      <div class="slider-container">
        <button class="slide-btn left" @click="slidePrev('rec')">‹</button>
        <div class="cards-wrapper">
          <div class="cards">
            <div
              v-for="book in recommendedBooks.slice(
                recIndex,
                recIndex + visibleCount
              )"
              :key="book.id"
              class="book-card"
              :style="cardStyleMap[book.id] || {}"
            >
              <router-link :to="`/books/${book.id}`" class="card-link">
                <img :src="book.cover_url" alt="cover" />
                <h4>{{ book.title }}</h4>
                <p>{{ book.author_name }}</p>
              </router-link>
            </div>
          </div>
        </div>
        <button class="slide-btn right" @click="slideNext('rec')">›</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, reactive } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import ColorThief from "colorthief";
import { useMainStore } from "@/stores/main";

// 배너 이미지
import banner1 from "@/assets/banners/banner1.png";
import banner2 from "@/assets/banners/banner2.png";
import banner3 from "@/assets/banners/banner3.png";
import banner4 from "@/assets/banners/banner4.png";
import banner5 from "@/assets/banners/banner5.png";

const router = useRouter();
const mainStore = useMainStore();
const isLoggedIn = computed(() => !!localStorage.token);

// 데이터
const bestSellers = ref([]);
const newBooks = ref([]);
const recommendedBooks = ref([]);

// 슬라이드 인덱스
const visibleCount = 7;
const bestIndex = ref(0);
const newIndex = ref(0);
const recIndex = ref(0);

// 카드 그라데이션 스타일 캐시
const cardStyleMap = reactive({});

// 책 데이터 + 그라데이션 적용
async function loadBooks() {
  const [bRes, nRes, rRes] = await Promise.all([
    axios.get("/api/books/?category=1"),
    axios.get("/api/books/?category=2"),
    axios.get("/api/books/?category=3"),
  ]);
  bestSellers.value = bRes.data.slice(0, 15);
  newBooks.value = nRes.data.slice(0, 15);
  recommendedBooks.value = rRes.data.slice(0, 15);

  // gradient 계산
  const all = [
    ...bestSellers.value,
    ...newBooks.value,
    ...recommendedBooks.value,
  ];
  for (let book of all) {
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

  await mainStore.fetchBestSellers();
  if (!isLoggedIn.value) {
    await mainStore.fetchAgeBased(20);
  }
}

// 배너 슬라이드
const bannerImages = [banner1, banner2, banner3, banner4, banner5];
const currentBanner = ref(0);
let bannerTimer = null;

onMounted(() => {
  loadBooks();
  bannerTimer = setInterval(() => {
    currentBanner.value = (currentBanner.value + 1) % bannerImages.length;
  }, 5000);
});

onBeforeUnmount(() => {
  clearInterval(bannerTimer);
});

// 라우팅
function goToBestsellers() {
  router.push({ name: "BestSellers" });
}

// 슬라이드 이동
function slidePrev(section) {
  if (section === "best" && bestIndex.value > 0) bestIndex.value--;
  if (section === "new" && newIndex.value > 0) newIndex.value--;
  if (section === "rec" && recIndex.value > 0) recIndex.value--;
}
function slideNext(section) {
  if (
    section === "best" &&
    bestIndex.value < bestSellers.value.length - visibleCount
  )
    bestIndex.value++;
  if (
    section === "new" &&
    newIndex.value < newBooks.value.length - visibleCount
  )
    newIndex.value++;
  if (
    section === "rec" &&
    recIndex.value < recommendedBooks.value.length - visibleCount
  )
    recIndex.value++;
}
</script>

<style scoped>
.main-page {
  padding: 2rem;
  color: #fff;
  background: transparent;
}

/* 배너 */
.banner-slider {
  width: 100%;
  aspect-ratio: 16 / 5;
  overflow: hidden;
  margin-bottom: 2rem;
}
.banner-track {
  display: flex;
  transition: transform 0.5s ease;
}
.banner-slide {
  flex: 0 0 100%;
}
.banner-slide img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  background: transparent;
}

/* 섹션 제목 */
.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
.more-link {
  font-size: 0.9rem;
  color: #aaa;
  text-decoration: none;
}

/* 카드 슬라이더 공통 */
.slider-container {
  position: relative;
  width: calc((clamp(100px, 15vw, 180px) * 7) + (0.5rem * 6));
  margin: 0 auto 2rem;
}
.cards-wrapper {
  overflow: hidden;
}
.cards {
  display: flex;
  gap: 0.5rem;
  transition: none;
}

/* 카드 */
.book-card {
  flex: 0 0 clamp(100px, 15vw, 180px);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
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
  color: rgb(255, 255, 255);
  padding: 0 0.5rem;
}
.book-card p {
  font-size: 0.75rem;
  color: rgb(221, 221, 221);
  margin: 0.25rem 0 0.5rem;
  padding: 0 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 좌우 버튼 */
.slide-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  color: #fff;
  font-size: 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  z-index: 10;
}
.slide-btn.left {
  left: -1.5rem;
}
.slide-btn.right {
  right: -1.5rem;
}
</style>
