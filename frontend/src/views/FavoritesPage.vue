<template>
  <div class="favorites-page">
    <h1>찜한 도서 목록</h1>

    <section v-if="!books.length" class="empty">
      <p>아직 찜한 도서가 없습니다.</p>
    </section>

    <div v-else class="book-grid">
      <div v-for="book in paginatedBooks" :key="book.id" class="book-card">
        <RouterLink :to="`/books/${book.id}`">
          <img :src="book.cover_url" alt="책 표지" class="book-image" />
          <p class="book-title">{{ book.title }}</p>
          <p class="book-author">{{ book.author_name }}</p>
        </RouterLink>
        <button class="delete-btn" @click="removeFavorite(book.id)">
          삭제
        </button>
      </div>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button @click="prevPage" :disabled="page === 1">◀ 이전</button>
      <span> {{ page }} / {{ totalPages }} </span>
      <button @click="nextPage" :disabled="page === totalPages">다음 ▶</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useProfileStore } from "@/stores/profile";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const profile = useProfileStore();
const auth = useAuthStore();

const books = ref([]);
const page = ref(1);
const perPage = 15;

const totalPages = computed(() => Math.ceil(books.value.length / perPage));

const paginatedBooks = computed(() => {
  const start = (page.value - 1) * perPage;
  return books.value.slice(start, start + perPage);
});

function prevPage() {
  if (page.value > 1) page.value--;
}
function nextPage() {
  if (page.value < totalPages.value) page.value++;
}

async function loadFavorites() {
  await profile.fetchMe();
  books.value = profile.favorites;
  if (page.value > totalPages.value) page.value = totalPages.value || 1;
}

async function removeFavorite(bookId) {
  if (!auth.token) return alert("로그인이 필요합니다.");
  try {
    await axios.delete(`/api/auth/users/me/favorites/${bookId}`, {
      headers: { Authorization: `Token ${auth.token}` },
    });
    await loadFavorites();
  } catch (err) {
    console.error(err);
    alert("삭제 중 오류가 발생했습니다.");
  }
}

onMounted(loadFavorites);
</script>

<style scoped>
.favorites-page {
  padding: 2rem;
  background: transparent;
  color: white;
}
.empty {
  text-align: center;
  color: #888;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(5, 200px);
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.book-card {
  width: 200px;
  background: #111;
  border-radius: 6px;
  overflow: hidden;
  text-align: center;
  position: relative;
}
.book-card a {
  text-decoration: none;
  color: inherit;
  display: block;
  padding: 0.5rem;
}
.book-image {
  width: 100%;
  height: 260px;
  object-fit: cover;
  border-radius: 4px;
}
.book-title {
  margin: 0.5rem 0 0.2rem;
  font-size: 1rem;
  font-weight: bold;
}
.book-author {
  margin: 0;
  font-size: 0.9rem;
  color: #ccc;
}
.delete-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(255, 0, 0, 0.7);
  border: none;
  color: white;
  font-size: 0.8rem;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  cursor: pointer;
}
.delete-btn:hover {
  background: rgba(255, 0, 0, 1);
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  color: #ccc;
}
.pagination button {
  background: none;
  border: 1px solid #555;
  color: white;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
