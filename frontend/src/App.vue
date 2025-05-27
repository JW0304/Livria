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
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Header from "@/components/Header.vue";
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

.app-layout {
  display: flex;
  transition: all 0.3s ease;
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
}
body {
  background-color: black;
  color: white;
  margin: 0;
  font-family: sans-serif;
}
</style>
