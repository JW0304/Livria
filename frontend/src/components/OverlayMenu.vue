<template>
  <div class="overlay" @click.self="$emit('close')">
    <nav class="menu">
      <h3 class="section-title">바로가기</h3>
      <ul>
        <li>
          <RouterLink to="/" :class="{ active: $route.path === '/' }"
            >메인</RouterLink
          >
        </li>
        <li>
          <RouterLink
            to="/bestsellers"
            :class="{ active: $route.path === '/bestsellers' }"
          >
            베스트 셀러
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/aria" :class="{ active: $route.path === '/aria' }">
            오늘의 아리아
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/newbook"
            :class="{ active: $route.path === '/newbook' }"
          >
            신착 도서
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/recommendations"
            :class="{ active: $route.path === '/recommendations' }"
          >
            블로거 추천 도서
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/reviews"
            :class="{ active: $route.path === '/reviews' }"
          >
            도서 리뷰
          </RouterLink>
        </li>
      </ul>

      <h3 class="section-title">장르</h3>
      <ul>
        <li>
          <RouterLink
            to="/genre/all"
            :class="{ active: $route.path === '/genre/all' }"
          >
            전체
          </RouterLink>
        </li>
        <li v-for="genre in genres" :key="genre.name">
          <RouterLink
            :to="`/genre/${genre.id}`"
            :class="{ active: $route.path === `/genre/${genre.id}` }"
          >
            {{ genre.name }}
          </RouterLink>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const genres = ref([]);

onMounted(async () => {
  try {
    const res = await axios.get("/api/genres/");
    genres.value = res.data;
  } catch (err) {
    console.error("장르 목록 로딩 실패:", err);
  }
});
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
}

.menu {
  width: 250px;
  background: #111;
  height: 100%;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
}

.section-title {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 0.8rem;
  margin-top: 2rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 1rem 0;
}

a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s;
  display: inline-block;
}

a.active {
  color: #b388f0;
}

a:hover {
  background: linear-gradient(to right, #d17df4, #8d5cf6);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
