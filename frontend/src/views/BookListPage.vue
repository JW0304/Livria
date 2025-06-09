<template>
  <div class="book-list-page">
    <h1>전체 도서 목록</h1>

    <BookList :books="store.books" />

    <Pagination
      :page="store.page"
      :total="store.total"
      :perPage="12"
      @change="store.fetchBooks"
    />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useBooksStore } from "@/stores/books";
import BookList from "@/components/BookList.vue";
import Pagination from "@/components/Pagination.vue";

const store = useBooksStore();

onMounted(() => {
  store.fetchBooks(1);
});
</script>

<style scoped>
.book-list-page {
  padding: 2rem;
  background: transparent;
  color: white;
}
</style>
