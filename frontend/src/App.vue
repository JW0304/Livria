<!-- <template>
  <div id="app">
    <Header @toggleMenu="menuOpen = !menuOpen" />
    <OverlayMenu v-if="menuOpen" @close="menuOpen = false" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template> -->

<template>
  <div :class="['app-layout', { 'sidebar-open': menuOpen }]">
    <OverlayMenu :isOpen="menuOpen" />
    <div class="main-wrapper">
      <Header @toggleMenu="menuOpen = !menuOpen" />
      <main class="main-content">
        <router-view />
      </main>
      <Footer />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import OverlayMenu from "@/components/OverlayMenu.vue";

const menuOpen = ref(false);
// 더 이상 auth.fetchMe()를 호출하지 않습니다.
</script>

<style>
/* * {
  font-family: "Nanum Gothic Coding", monospace;
  font-weight: 400;
  font-style: normal;
} */

/* .app-layout {
  display: flex;
  transition: all 0.3s ease;
  height: 100vh;
  background: linear-gradient(
    135deg,
    #9c4dff,
    #ff6fd5,
    #fbcf46
  );
  background-size: 400% 400%;
  animation: gradientBG 10s ease infinite;
} */

/* 레이아웃 설정 */

.sidebar-open .main-wrapper {
  margin-left: 240px;
}

.main-content {
  margin-top: 20px;
  padding: 2rem;
  position: relative; /* 배경이 콘텐츠 위로 오지 않도록 */
}

/* 전체 HTML 및 Body의 높이를 100%로 설정 */
html,
body {
  height: 100%;
  margin: 0;
}

body {
  background-color: transparent; /* body는 투명으로 처리 */
  color: rgb(0, 0, 0);
  margin: 0;
  font-family: sans-serif;
}

header {
  z-index: 10; /* 헤더를 배경 위로 올림 */
}

.sidebar {
  z-index: 20; /* 사이드바가 배경보다 위에 오도록 설정 */
}

/* 애니메이션 정의 */
@keyframes gradientBG {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
