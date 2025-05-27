<template>
  <div class="category-page">
    <h1>{{ route.params.name }} 카테고리</h1>

    <div class="book-grid">
      <div v-for="book in books" :key="book.id" class="book-card">
        <img :src="book.cover_url" alt="cover" />
        <h3>{{ book.title }}</h3>
        <p>{{ book.author_name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const books = ref([]);

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/genres/1/");
    const match = data.find((cat) => cat.name === route.params.name);

    if (match) {
      books.value = match.books;
    } else {
      books.value = [];
    }
  } catch (err) {
    console.error("카테고리 불러오기 실패", err);
  }
});
</script>

<style scoped>
.category-page {
  padding: 2rem;
  background: transparent;
  color: white;
}
.book-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
}
.book-card {
  background: #111;
  padding: 1rem;
  border-radius: 0.5rem;
}
.book-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>
