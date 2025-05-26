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
          <p class="author">{{ book.author_name || "저자 미상" }}</p>
          <ul class="meta">
            <li>ISBN: {{ book.isbn }}</li>
            <li>출판일: {{ book.pub_date || "출판일 미상" }}</li>
            <li>장르: {{ book.genre_name || "장르 미상" }}</li>
          </ul>
          <p class="summary">{{ book.description || "줄거리 없음" }}</p>
        </div>
        <div class="icons">
          <span>♡</span>
          <span>🔒</span>
        </div>
      </section>

      <!-- 작가 소개 -->
      <section class="author-info">
        <div class="author-avatar">
          <img
            :src="book.author_image_url"
            alt="작가 사진"
            class="avatar-img"
            @error="(e) => (e.target.src = '/images/default_author.png')"
          />
        </div>
        <div class="author-text">
          <h3 class="author-name">{{ book.author_name }}</h3>
          <div class="author-summary-box">
            <p class="author-summary">
              {{ book.author_summary || "작가 소개가 없습니다." }}
            </p>
          </div>
        </div>
      </section>

      <!-- 태그 -->
      <section class="emotion-tags">
        <h2>오늘 당신의 감정은?</h2>
        <div class="tag-list">
          <button
            v-for="tag in allTags"
            :key="tag.id"
            :class="{
              selected: selectedTagIds.includes(tag.id),
              unselected: !selectedTagIds.includes(tag.id),
            }"
            @click="toggleTag(tag.id)"
          >
            {{ tag.name }}
          </button>
        </div>
        <div v-if="isLoggedIn" class="edit-tags">
          <button @click="saveEmotionTags">태그 수정</button>
        </div>
      </section>

      <!-- 음악 추천 -->
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

      <!-- 댓글 -->
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
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const isLoggedIn = computed(() => !!localStorage.token);
const selectedTagIds = ref([]);
const allTags = ref([]);

const route = useRoute();
const book = ref(null);

onMounted(async () => {
  try {
    const res = await axios.get(
      `http://localhost:8000/api/books/${route.params.id}/`
    );
    book.value = res.data;

    const tagRes = await axios.get("/api/emotion-tags/");
    allTags.value = tagRes.data;

    if (isLoggedIn.value) {
      const userRes = await axios.get("/api/auth/users/me", {
        headers: { Authorization: `Token ${localStorage.getItem("token")}` },
      });
      selectedTagIds.value = userRes.data.emotion_tags.map((tag) => tag.id);
    } else {
      const defaultTag = tagRes.data.find(
        (tag) => tag.name === "사랑과 그리움"
      );
      if (defaultTag) selectedTagIds.value = [defaultTag.id];
    }
  } catch (err) {
    console.error("책 상세 정보 불러오기 실패:", err);
  }
});

function toggleTag(tagId) {
  if (selectedTagIds.value.includes(tagId)) {
    selectedTagIds.value = selectedTagIds.value.filter((id) => id !== tagId);
  } else {
    selectedTagIds.value.push(tagId);
  }
}

async function saveEmotionTags() {
  try {
    await axios.patch(
      "/api/auth/users/me/",
      { emotion_tags: selectedTagIds.value },
      {
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      }
    );
    alert("감정 태그가 수정되었습니다!");
  } catch (err) {
    console.error("태그 저장 실패:", err);
  }
}
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
.emotion-tag {
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
.author-info {
  display: flex;
  align-items: flex-start;
  background-color: #1e1e1e;
  padding: 1rem;
  border-radius: 0.5rem;
}
.author-avatar {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #555;
  overflow: hidden;
  margin-right: 1rem;
}
.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.author-text {
  flex-grow: 1;
}
.author-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  margin-bottom: 0.5rem;
}
.author-summary-box {
  background-color: #333;
  padding: 0.8rem;
  border-radius: 0.5rem;
  color: #ccc;
  font-size: 0.95rem;
  white-space: pre-line;
}
.selected {
  background-color: #a96acc;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  margin: 0.3rem;
}
.unselected {
  background-color: #444;
  color: #ccc;
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  margin: 0.3rem;
}
</style>
