<template>
  <div class="search-page">
    <div class="filters">
      <!-- <div class="filter-group">
        <p class="filter-title">태그</p>
        <button
          v-for="tag in tags"
          :key="tag"
          :class="{ active: selectedTags.includes(tag) }"
          @click="toggleTag(tag)"
        >
          {{ tag }}
        </button>
      </div> -->

      <!-- <div class="filter-group">
        <p class="filter-title">카테고리</p>
        <button
          v-for="category in categories"
          :key="category"
          :class="{ active: selectedCategory === category }"
          @click="selectCategory(category)"
        >
          {{ category }}
        </button>
      </div> -->
    </div>

    <section v-if="loading">불러오는 중...</section>
    <section v-else-if="!filteredBooks.length">검색 결과가 없습니다.</section>
    <section class="book-grid" v-else>
      <div v-for="book in filteredBooks" :key="book.id" class="book-card">
        <img :src="book.cover_url" alt="book cover" />
        <p class="book-title">{{ book.title }}</p>
        <p class="book-author">{{ book.author_name }}</p>
      </div>
    </section>

    <div class="pagination">
      <button class="arrow" @click="prevPage">◀</button>
      <button class="arrow" @click="nextPage">▶</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const query = ref("");
const route = useRoute();
const loading = ref(false);
const results = ref([]);

const fetchSearchResults = async (query) => {
  loading.value = true;
  try {
    const res = await axios.get("/api/books/?search/", {
      params: { q: query },
    });
    results.value = res.data.books; // ✅ API 응답 구조 기준
  } catch (err) {
    console.error("검색 실패:", err);
  } finally {
    loading.value = false;
  }
};

function searchBooks() {
  if (!query.value) return;

  axios
    .get(`/api/books/?search=${query.value}`)
    .then((res) => {
      books.value = res.data.results || res.data; // pagination 여부에 따라 분기
    })
    .catch((err) => {
      console.error("검색 실패:", err);
    });
}

onMounted(() => {
  if (route.query.q) {
    fetchSearchResults(route.query.q);
  }
});

watch(
  () => route.query.q,
  (newQuery) => {
    console.log("watch triggered, query:", newQuery);
    if (newQuery) fetchSearchResults(newQuery);
  }
);

const tags = [
  "슬픔과 외로움",
  "사랑과 그리움",
  "위로와 평안",
  "에너지와 고조",
  "몽환적이고 감성적인",
];
const categories = [
  "소설/시/희곡",
  "경제/경영",
  "자기계발",
  "인문/교양",
  "취미/실용",
  "어린이/청소년",
  "과학",
];

const selectedTags = ref([]);
const selectedCategory = ref(null);

const filteredBooks = computed(() => {
  let books = results.value;

  if (selectedTags.value.length) {
    books = books.filter((book) =>
      selectedTags.value.every((tag) => book.tags?.includes(tag))
    );
  }

  if (selectedCategory.value) {
    books = books.filter((book) => book.category === selectedCategory.value);
  }

  return books.slice(0, 12); // 간단한 페이징
});

function toggleTag(tag) {
  const idx = selectedTags.value.indexOf(tag);
  if (idx > -1) selectedTags.value.splice(idx, 1);
  else selectedTags.value.push(tag);
}
function selectCategory(cat) {
  selectedCategory.value = cat;
}

function prevPage() {}
function nextPage() {}
</script>

<style scoped>
.search-page {
  background-color: #111;
  color: white;
  padding: 2rem;
  min-height: 100vh;
}
.filters {
  margin-bottom: 2rem;
}
.filter-group {
  margin-bottom: 1rem;
}
.filter-title {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #aaa;
}
button {
  margin: 0.3rem;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 20px;
  background: #ccc;
  color: black;
  cursor: pointer;
  font-size: 0.9rem;
}
button.active {
  background: #a86ee0;
  color: white;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1.5rem;
}
.book-card {
  background: white;
  color: black;
  padding: 0.5rem;
  border-radius: 8px;
  text-align: center;
}
.book-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
}
.book-title {
  font-weight: bold;
}
.pagination {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}
.arrow {
  background: #444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
}
</style>
