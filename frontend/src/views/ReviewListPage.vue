<template>
  <div class="review-page">
    <header class="review-header">
      <h1>리뷰 목록 페이지</h1>
    </header>

    <div class="review-grid">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="myCard"
        @click="goToDetail(review.book_id)"
      >
        <div class="innerCard">
          <!-- 앞면: 책 표지 전체 -->
          <div class="frontSide">
            <img
              :src="review.book_cover_url"
              alt="책 커버"
              class="cover-full"
            />
          </div>

          <!-- 뒷면: 프로필 + 닉네임 + 리뷰 + 날짜 -->
          <div class="backSide">
            <img :src="review.user_avatar" alt="프로필" class="avatar" />
            <p class="username">{{ review.user }}</p>
            <p class="review-snippet">"{{ review.content }}"</p>
            <p class="date">{{ formatDate(review.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const reviews = ref([]);

async function fetchReviews() {
  const { data } = await axios.get("/api/reviews/");
  reviews.value = data;
}

function goToDetail(bookId) {
  router.push(`/books/${bookId}`);
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString();
}

onMounted(fetchReviews);
</script>

<style scoped>
.review-page {
  padding: 2rem;
  background: transparent;
  color: white;
}

.review-header h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.review-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
  justify-content: center;
}

.myCard {
  background-color: transparent;
  width: 140px;
  height: 200px;
  perspective: 1000px;
}

.innerCard {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
  cursor: pointer;
}

.myCard:hover .innerCard {
  transform: rotateY(180deg);
}

.frontSide,
.backSide {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 1rem;
  overflow: hidden;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0.3em rgba(255, 255, 255, 0.3);
}

.frontSide {
  background: #000;
}

.cover-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 1rem;
}

/* 뒷면 스타일 */
.backSide {
  transform: rotateY(180deg);
  background: linear-gradient(160deg, #0093e9 0%, #80d0c7 100%);
  color: white;
  padding: 0.6rem;
  font-size: 0.75rem;
  gap: 0.4rem;
  text-align: center;
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
}

.username {
  font-size: 0.85rem;
  font-weight: bold;
}

.review-snippet {
  font-size: 0.7rem;
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* 표준 속성도 같이 써주기 (지원하는 브라우저만 적용됨) */
  line-clamp: 2;
  text-overflow: ellipsis;
  max-width: 100%;
}

.date {
  font-size: 0.65rem;
  opacity: 0.8;
}
</style>
