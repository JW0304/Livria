<template>
  <header class="app-header">
    <!-- 좌측: 햄버거 + 로고 -->
    <div class="left">
      <button @click="$emit('toggleMenu')" class="hamburger">☰</button>
      <RouterLink to="/" class="logo">
        <img src="@/assets/Logo.png" alt="Livria Logo" class="logo-img" />
        <span class="logo-text">Livria</span>
      </RouterLink>
    </div>

    <!-- 중앙: 검색창 -->
    <form @submit.prevent="onSearch" class="search-bar">
      <input v-model="query" placeholder="책 제목/작가 검색" />
      <button type="submit">🔍</button>
    </form>

    <!-- 우측: 인증 버튼 -->
    <div class="auth-buttons">
      <template v-if="auth.user">
        <RouterLink to="/mypage" class="nickname">
          <img :src="avatarUrl" class="avatar" />
          {{ auth.user.nickname }}님
        </RouterLink>
        <button @click="logout">로그아웃</button>
      </template>
      <template v-else>
        <button @click="goLogin">로그인</button>
        <button @click="goSignup">회원가입</button>
      </template>
    </div>

  </header>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();
const query = ref("");

const isLoggedIn = computed(() => !!auth.token);
const username = computed(() => auth.user?.nickname || "마이페이지");

const avatarUrl = computed(() => {
  const defaultAvatar = auth.user?.default_avatar || 'default1'
  return `/avatars/${defaultAvatar}.png`
})

const onSearch = () => {
  if (query.value.trim()) {
    router.push({ name: "Search", query: { q: query.value.trim() } });
  }
};

function goLogin() {
  router.push("/login");
}

function goSignup() {
  router.push("/signup");
}

const logout = () => {
  auth.logout()
  router.push('/')
}

</script>

<style scoped>
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.auth-buttons button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

.nickname {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
.nickname:hover {
  text-decoration: underline;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: black;
  color: white;
  gap: 1rem;
}

/* 좌측 정렬 */
.left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.logo-text {
  font-weight: bold;
  font-size: 1.5rem;
  color: #b388f0;
}

/* 중앙 검색창 */
.search-bar {
  display: flex;
  align-items: center;
  background-color: #333;
  border-radius: 2rem;
  padding: 0.3rem 1rem;
  flex-grow: 1;
  max-width: 400px;
}

.search-bar input {
  background: transparent;
  border: none;
  color: white;
  outline: none;
  flex-grow: 1;
  padding: 0.3rem;
  font-size: 1rem;
}

.search-bar button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
}

/* 우측 인증 버튼 */
.auth-buttons {
  display: flex;
  gap: 1rem;
}

.hamburger {
  background: none;
  color: white;
  font-size: 1.5rem;
  border: none;
}
</style>
