<template>
  <aside class="sidebar">
    <nav>
      <RouterLink to="/">홈</RouterLink>
      <RouterLink to="/books">도서 목록</RouterLink>
      <RouterLink to="/recommendations">추천</RouterLink>
      <RouterLink to="/mypage">마이페이지</RouterLink>
      <!-- 더 추가 가능 -->
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 200px;
  background: #222;
  color: white;
  height: 100vh;
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
}
.sidebar a {
  display: block;
  color: white;
  margin-bottom: 1rem;
  text-decoration: none;
}
</style>
