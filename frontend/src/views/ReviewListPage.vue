<template>
  <div class="review-page">
    <header class="review-header">
      <h1>리뷰 목록 페이지</h1>
    </header>

    <section class="review-grid">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="review-card"
        @click="goToDetail(review.id)"
      >
        <img :src="review.cover" alt="cover" />
        <div class="review-info">
          <p class="review-title">{{ review.title }}</p>
          <p class="review-subtitle">{{ review.subtitle }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const reviews = ref([
  {
    id: 1,
    title: 'BAC',
    subtitle: 'Love Me',
    cover: '/images/book1.png',
  },
  {
    id: 2,
    title: 'BAC',
    subtitle: 'Love Me',
    cover: '/images/book2.png',
  },
  {
    id: 3,
    title: 'BAC',
    subtitle: 'Love Me',
    cover: '/images/book3.png',
  },
  {
    id: 4,
    title: 'BAC',
    subtitle: 'Love Me',
    cover: '/images/book4.png',
  },
  {
    id: 5,
    title: 'BAC',
    subtitle: 'Love Me',
    cover: '/images/book5.png',
  },
  {
    id: 6,
    title: 'BAC',
    subtitle: 'Love Me',
    cover: '/images/book6.png',
  },
])

function goToDetail(id) {
  router.push(`/reviews/${id}`)
}
</script>

<style scoped>
.review-page {
  background: #111;
  color: white;
  padding: 1rem;
}
.review-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  justify-items: center;
  margin-top: 2rem;
}
.review-card {
  background: #fe8851;
  border-radius: 16px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  width: 150px;
  height: 220px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s;
}
.review-card:hover {
  transform: scale(1.05);
}
.review-card img {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  object-fit: cover;
}
.review-info {
  position: absolute;
  text-align: center;
  color: white;
  z-index: 2;
}
.review-title {
  font-weight: bold;
  font-size: 1.2rem;
}
.review-subtitle {
  font-size: 0.9rem;
  opacity: 0.8;
}
</style>
