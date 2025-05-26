<template>
  <div id="app">
    <Header @toggleMenu="menuOpen = !menuOpen" />
    <OverlayMenu v-if="menuOpen" @close="menuOpen = false" />
    <main class="main-content">
      <router-view />
    </main>
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
