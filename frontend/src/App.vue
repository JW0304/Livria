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
</script>

<style>
@font-face {
  font-family: "GongGothicMedium";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_20-10@1.0/GongGothicMedium.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: "LINESeedKR-Bd";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_11-01@1.0/LINESeedKR-Bd.woff2")
    format("woff2");
  font-weight: 300;
  font-style: normal;
}

@font-face {
  font-family: "NoonnuBasicGothicRegular";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noon-2410@1.0/NoonnuBasicGothicRegular.woff2")
    format("woff2");
  font-weight: 300;
  font-style: normal;
}

@font-face {
  font-family: "KimjungchulMyungjo-Bold";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2302_01@1.0/KimjungchulMyungjo-Bold.woff2")
    format("woff2");
  font-weight: 700;
  font-style: normal;
}

/* --------------------------------------------------
   전역 가로 스크롤 제거, body에 고정 그라데이션
   -------------------------------------------------- */
html,
body {
  height: 100%;
  margin: 0;
  overflow-x: hidden;
}
body {
  background: linear-gradient(
    45deg,
    #45023e,
    #000000,
    hsl(277, 94%, 13%),
    #24043b5c
  );
  background-size: 400% 400%;
  background-attachment: fixed;
  animation: gradientBG 15s ease infinite;
  font-family: sans-serif;
  color: #000;
}

/* 최상위 레이아웃 */
.app-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  transition: all 0.3s ease;
}

/* 사이드바 닫힘 시 메인/푸터 영역이 64px 밀려 나오도록 */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 64px;
  transition: margin-left 0.3s ease;
}

/* 사이드바 열림 시(250px) */
.sidebar-open .main-wrapper {
  margin-left: 250px;
}

/* 헤더 / 콘텐츠 / 푸터 배치, 가로 스크롤 제거 */
.main-content {
  flex: 1;
  margin-top: 20px;
  padding: 2rem;
  position: relative;
  overflow-x: hidden;
}

/* z-index 유지 */
header {
  z-index: 10;
}
.sidebar {
  z-index: 20;
}

/* 그라데이션 애니메이션 */
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
