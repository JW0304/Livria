<template>
  <div class="overlay" @click.self="$emit('close')">
    <nav class="menu">
      <h3 class="section-title">바로가기</h3>
      <ul>
        <li><RouterLink to="/" exact>메인</RouterLink></li>
        <li><RouterLink to="/bestsellers">베스트 셀러</RouterLink></li>
        <li><RouterLink to="/bestsellers">오늘의 아리아</RouterLink></li>
        <li><RouterLink to="/newbook">신착 도서</RouterLink></li>
        <li><RouterLink to="/recommendations">블로거 추천 도서</RouterLink></li>
        <li><RouterLink to="/reviews">도서 리뷰</RouterLink></li>
      </ul>

      <h3 class="section-title">카테고리</h3>
      <ul>
        <li v-for="category in categories" :key="category.name">
          <RouterLink
            :to="`/genres/${category.name}`"
            :class="{ active: $route.path === `/category/${category.name}` }"
          >
            {{ category.name }}
          </RouterLink>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
const route = useRoute();

const categories = [
  { name: "전체" },
  { name: "소설/시/희곡" },
  { name: "경제/경영" },
  { name: "자기계발" },
  { name: "인문/교양" },
  { name: "취미/실용" },
  { name: "어린이/청소년" },
  { name: "과학" },
];
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

/* 현재 선택된 메뉴: 보라색 */
a.active {
  color: #b388f0;
}

/* hover 시 그라데이션 효과 */
a:hover {
  background: linear-gradient(to right, #d17df4, #8d5cf6);
  background-clip: text; /* 표준 속성 */
  -webkit-background-clip: text; /* 크롬, 사파리 등 웹킷 계열 */
  -webkit-text-fill-color: transparent;
}
</style>
