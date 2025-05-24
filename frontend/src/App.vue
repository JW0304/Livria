<template>
  <div id="app">
    <Header @toggleMenu="menuOpen = !menuOpen"></Header>
    <OverlayMenu v-if="menuOpen" @close="menuOpen = false" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from '@/components/Header.vue'
import OverlayMenu from './components/OverlayMenu.vue'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

onMounted(() => {
  auth.fetchMe()
})

const menuOpen = ref(false)
</script>

<style>
.main-content {
  margin-top: 60px; /* 헤더가 고정이면 */
  padding: 2rem;
}

body {
  background-color: black;
  color: white;
  margin: 0;
  font-family: sans-serif;
}
</style>
