<template>
  <div class="main-page">
    <section>
      <h2 @click="goToBestsellers" style="cursor: pointer">
        베스트 셀러
        <router-link to="/bestsellers" class="more-link">더보기</router-link>
      </h2>
      <div class="book-grid">
        <RouterLink
          v-for="book in bestSellers"
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

    <!-- <section v-if="isLoggedIn">
      <h2>오늘의 아리아</h2>
      <BookList :books="mainStore.ageRecs" />
    </section> -->

    <section>
      <h2>새로 도착한 도서</h2>
      <router-link to="/newbook" class="more-link">더보기</router-link>
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
      <h2>블로거 추천 도서</h2>
      <router-link to="/recommendations" class="more-link">더보기</router-link>
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

onMounted(async () => {
  try {
    const bestsellerRes = await axios.get("/api/books/?category=1");
    bestSellers.value = bestsellerRes.data.slice(0, 6); // 상위 3개

    const newBookRes = await axios.get("/api/books/?category=2");
    newBooks.value = newBookRes.data.slice(0, 6); // 신간도 상위 3개 (원하면 더)

    const recommendationsRes = await axios.get("/api/books/?category=3");
    recommendedBooks.value = recommendationsRes.data.slice(0, 6);
  } catch (err) {
    console.error("도서 데이터 불러오기 실패:", err);
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
</script>

<style scoped>
.book-card {
  background: black;
  border-radius: 8px;
  padding: 0.5rem;
  text-align: center;
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit; /* 글자색 상속 */
  display: block;
}
.book-card:hover {
  background-color: #222;
  transform: scale(1.02);
  transition: all 0.2s;
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
}
.book-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  justify-items: center;
}
.book-card {
  background: black;
  border-radius: 8px;
  padding: 0.5rem;
  text-align: center;
}
.book-card img {
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
}

.more-link {
  font-size: 0.9rem;
  color: #aaa;
  cursor: pointer;
}
</style>
