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
.app-layout {
  display: flex;
  flex-direction: column;
  position: relative; /* 자식 요소가 절대 위치를 가질 수 있도록 */
  min-height: 100vh; /* 화면 최소 높이를 100vh로 설정 */
  background: linear-gradient(
    135deg,
    #120127,
    /* 검정색 */ #000000,
    /* 보라색 */ #2b0244,
    #6b0262
  );
  background-size: 400% 400%;
  animation: gradientBG 10s ease infinite; /* 그라데이션 애니메이션 */
  z-index: -1; /* 배경이 콘텐츠 아래로 가도록 설정 */
}
.main-wrapper {
  flex-grow: 1;
  transition: margin-left 0.3s ease;
  margin-left: 60px;
}

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

/* 그라데이션 배경 애니메이션 */
.app-layout::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #360238, #000000, #190227, #c073d3);
  background-size: 400% 400%; /* 그라데이션 영역 확대 */
  animation: gradientBG 10s ease infinite; /* 그라데이션 애니메이션 */
  z-index: -100; /* 배경이 콘텐츠 뒤로 가도록 설정 */
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
