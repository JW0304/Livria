<template>
  <div class="book-card" @click="$emit('click', book.id)">
    <img :src="book.cover_url" :alt="book.title" class="cover" />
    <div class="title">{{ book.title }}</div>
    <div class="author">{{ book.author.name }}</div>
  </div>
</template>

<script setup>
const props = defineProps({
  book: Object
})
</script>

<style scoped>
.book-card {
  width: 160px;
  cursor: pointer;
  transition: transform 0.2s;
}
.book-card:hover {
  transform: scale(1.03);
}
.cover {
  width: 100%;
  border-radius: 6px;
  object-fit: cover;
}
.title {
  margin-top: 0.5rem;
  font-weight: bold;
  color: white;
  font-size: 0.95rem;
}
.author {
  font-size: 0.8rem;
  color: #bbb;
}
</style>
