<template>
  <div class="app-layout">
    <Header @toggleMenu="menuOpen = !menuOpen" />
    <OverlayMenu :isOpen="menuOpen" />
    <div class="main-wrapper">
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
/* 전체 레이아웃 */
.app-layout {
  display: flex;
  flex-direction: column;
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.app-layout::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #120127, #000000, #2b0244, #6b0262);
  background-size: 400% 400%;
  animation: gradientBG 10s ease infinite;
  z-index: -2; /* 배경을 콘텐츠보다 뒤로 */
  pointer-events: none; /* 배경 클릭 무시 */
}

/* 메인 내용 */
.main-wrapper {
  position: relative;
  z-index: 1;
  margin-left: 0; /* 사이드바 열릴 때 밀리도록 설정 */
  transition: margin-left 0.3s ease; /* 사이드바 애니메이션 효과 */
}

/* 사이드바 */
.overlay-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  background: #111;
  width: 64px;
  transition: width 0.3s ease;
  overflow: hidden;
  z-index: 1000; /* 사이드바가 배경보다 앞에 오도록 설정 */
}

.overlay-sidebar.open {
  width: 250px;
}

/* 햄버거 버튼 */
.hamburger-btn {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}

/* 메인 콘텐츠 */
.main-content {
  margin-top: 20px;
  padding: 2rem;
  position: relative;
  z-index: 1; /* 콘텐츠가 배경 위에 오도록 설정 */
}

header {
  position: relative;
  z-index: 1001; /* 헤더가 배경보다 앞에 오도록 설정 */
}

footer {
  position: relative;
  z-index: 1001;
}

/* 애니메이션: 배경 그라데이션 */
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
