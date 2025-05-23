<template>
  <div class="book-detail" v-if="book">
    <!-- 책 정보 -->
    <main>
      <section class="book-info">
        <div class="cover">
          <img :src="book.cover_url" alt="cover" class="cover-img" />
        </div>
        <div class="info">
          <h2>{{ book.title }}</h2>
          <p class="author">{{ book.author_name || '작자 미상' }}</p>
          <ul class="meta">
            <li>ISBN: {{ book.isbn }}</li>
            <li>출판일: {{ book.pub_date || '정보 없음' }}</li>
            <li>장르 ID: {{ book.category }}</li>
            <li>추천 수: {{ book.global_recommend_count }}</li>
          </ul>
          <p class="summary">{{ book.description || '줄거리 없음' }}</p>
        </div>
        <div class="icons">
          <span>♡</span>
          <span>🔒</span>
        </div>
      </section>

      <!-- 작가 소개 -->
      <section class="author-info">
        <div class="avatar">
          <img
            v-if="book.author_info?.image_url"
            :src="book.author_info.image_url"
            alt="author"
            class="author-img"
          />
        </div>
        <div class="bio">
          <h3>작가 소개</h3>
          <p>{{ book.author_info?.summary || '작가 소개 정보 없음' }}</p>
        </div>
      </section>

      <!-- 태그 (현재 고정) -->
      <section class="tags">
        <h4>현재 태그</h4>
        <div class="tag-list">
          <span class="tag">슬픔과 외로움</span>
          <span class="tag">사랑과 그리움</span>
          <span class="tag">위로와 울먹</span>
        </div>
      </section>

      <!-- 음악 추천 (현재 고정) -->
      <section class="music">
        <div class="music-card">
          <h5>🎵 Soldiers Rage - The Mechanic</h5>
          <p>3:21</p>
          <div class="actions">
            <button>👍</button>
            <span>14</span>
            <button>👎</button>
          </div>
        </div>
      </section>

      <!-- 댓글 (현재 고정) -->
      <section class="comments">
        <h4>감상평</h4>
        <div class="comment-box">
          <p>이거 실화냐 가슴이 웅장해진다..</p>
          <small>By 사용자명</small>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const book = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/books/${route.params.id}/`)
    book.value = res.data
  } catch (err) {
    console.error('책 상세 정보 불러오기 실패:', err)
  }
})
</script>

<style scoped>
.book-detail {
  color: white;
  background: #1a1a1a;
  padding: 2rem;
}
.book-info {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}
.cover-img {
  width: 200px;
  height: 300px;
  object-fit: cover;
  border-radius: 6px;
}
.icons {
  font-size: 1.5rem;
}
.author-info,
.music,
.tags,
.comments {
  margin-top: 2rem;
}
.author-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ccc;
}
.tag {
  background: #666;
  padding: 0.3rem 0.6rem;
  margin: 0.2rem;
  border-radius: 0.5rem;
}
.music-card {
  background: linear-gradient(to right, #7f00ff, #e100ff);
  padding: 1rem;
  border-radius: 1rem;
  color: white;
}
.comment-box {
  background: linear-gradient(to right, #ff758c, #ff7eb3);
  padding: 1rem;
  border-radius: 1rem;
}
</style>
