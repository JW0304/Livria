<template>
  <div class="book-list">
    <BookCard
      v-for="book in books"
      :key="book.id"
      :book="book"
      @click="goToDetail"
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import BookCard from './BookCard.vue'

const props = defineProps({
  books: Array
})

const router = useRouter()

function goToDetail(bookId) {
  router.push(`/books/${bookId}`)
}
</script>

<style scoped>
.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
  padding: 1rem 0;
}
</style>
