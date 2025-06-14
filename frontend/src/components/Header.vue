<template>
  <header class="app-header">
    <!-- 좌측: 햄버거 + 로고 -->
    <div class="left">
      <button @click="$emit('toggleMenu')" class="hamburger">
        <AlignJustify class="hamburger-icon" />
      </button>
      <RouterLink to="/" class="logo">
        <img src="@/assets/whiteLogo.png" alt="Livria Logo" class="logo-img" />
        <span class="logo-text">Livria</span>
      </RouterLink>
    </div>

    <!-- 중앙: 검색창 -->
    <!-- <form @submit.prevent="onSearch" class="search-bar">
      <input v-model="query" placeholder="책 제목 / 작가 검색" />
      <button type="submit">🔍</button>
    </form> -->

    <div class="search-bar">
      <input
        v-model="query"
        placeholder="책 제목 / 작가 검색"
        @keydown.enter.prevent="onSearch"
      />
      <span class="search-icon">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="lucide"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#999"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </span>
    </div>

    <!-- 우측: 인증 버튼 -->
    <div class="auth-buttons">
      <template v-if="auth.user">
        <RouterLink to="/mypage" class="nickname">
          <img :src="avatarUrl" class="avatar" />
          {{ profile.nickname || auth.user.nickname }} 님
        </RouterLink>
        <button @click="logout" class="brand-text">로그아웃</button>
      </template>
      <template v-else>
        <button @click="goLogin" class="brand-text">로그인</button>
        <button @click="goSignup" class="brand-text">회원가입</button>
      </template>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useProfileStore } from "@/stores/profile";
import { AlignJustify } from "lucide-vue-next";

const router = useRouter();
const auth = useAuthStore();
const profile = useProfileStore();

const query = ref("");

// 앱이 처음 로드될 때, 토큰이 있으면 프로필 정보를 미리 가져옵니다.
onMounted(() => {
  if (auth.token) {
    profile.fetchMe().catch(() => {
      // 실패해도 헤더는 로그인 상태 유지
    });
  }
});

// 검색
const onSearch = () => {
  if (query.value.trim()) {
    router.push({ name: "Search", query: { q: query.value.trim() } });
  }
};

// 로그인/회원가입/로그아웃
function goLogin() {
  router.push("/login");
}
function goSignup() {
  router.push("/signup");
}
const logout = () => {
  auth.logout();
  router.push("/");
};

// 헤더용 아바타 URL: 프로필 스토어의 avatarUrl이 우선, 없으면 defaultAvatar로
const avatarUrl = computed(() => {
  return (
    profile.avatarUrl || `/avatars/${profile.defaultAvatar || "default1"}.png`
  );
});
</script>

<style scoped>
.brand-text {
  font-family: "LINESeedKR-Bd", sans-serif;
  font-size: 20px;
  color: #888;
}

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
  margin-right: 2rem;
}
.auth-buttons button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

.nickname {
  font-family: "LINESeedKR-Bd", sans-serif;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: white;
  text-decoration: none;
  font-weight: bold;
}
.nickname:hover {
  text-decoration: underline;
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px; /* 원하는 높이 조절 */
  background: black;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  z-index: 1000; /* 다른 요소보다 위로 */
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); /* 선택 사항 */
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
  gap: 0.3rem;
  text-decoration: none;
  opacity: 0.85; /* 0.0(완전 투명) ~ 1.0(완전 불투명) */
}

.logo-img {
  width: 34px;
  height: 34px;
  object-fit: contain;
  margin-left: 0.6rem;
}

.logo-text {
  /* font-weight: bold; */
  font-family: "GongGothicMedium", sans-serif;
  font-size: 1.4rem;
  margin-top: 0.2rem;
  margin-left: 0.2rem;
  color: #e4e4e4;
  /* background: linear-gradient(to right, #e718b4, #4cc2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; */
}

/* 중앙 검색창 */
.search-bar {
  display: flex;
  align-items: center;
  background-color: #222222;
  border-radius: 2rem;
  margin-top: 0.15rem;
  padding: 0.3rem 1rem;
  max-width: 400px;
  width: 100%;
  gap: 0.5rem;
}

.search-bar input {
  background: transparent;
  border: none;
  color: white;
  outline: none;
  flex-grow: 1;
  font-size: 1rem;
}

.search-bar input::placeholder {
  color: #888;
}

.search-icon svg {
  width: 20px;
  height: 20px;
  stroke: #aaa;
  flex-shrink: 0;
}

/* .search-bar {
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
} */

.hamburger {
  background: none;
  border: none;
  cursor: pointer;
  padding: 1rem;
  margin-left: 1rem;
}

.hamburger-icon {
  width: 24px;
  height: 24px;
  color: white;
}
</style>
