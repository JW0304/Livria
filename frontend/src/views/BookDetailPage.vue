<template>
  <div class="book-detail" v-if="book">
    <main>
      <!-- 책 정보 -->
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
      <!-- <section class="tags">
        <h2>오늘 당신의 감정은?</h2>
        <div class="tag-list">
          <button
            v-for="tag in Tags"
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
      </section> -->

      <!-- 태그 선택 -->
      <section class="tags">
        <h2>오늘 당신의 감정은?</h2>
        <div class="tag-list">
          <span
            v-for="tag in emotionTags"
            :key="tag.id"
            class="tag"
            :class="{ selected: tag.name === selectedTag }"
            @click="selectTag(tag.name)"
          >
            {{ tag.name }}
          </span>
        </div>
      </section>

      <!-- 음악 카드 리스트 -->
      <section class="music">
        <div v-for="music in filteredMusics" :key="music.id" class="card">
          <div class="top">
            <div class="pfp">
              <div class="playing">
                <div class="greenline line-1"></div>
                <div class="greenline line-2"></div>
                <div class="greenline line-3"></div>
                <div class="greenline line-4"></div>
                <div class="greenline line-5"></div>
              </div>
            </div>
            <div class="texts">
              <p class="title-1">{{ music.tag }}</p>
              <p class="title-2">{{ book.title }}</p>
            </div>
          </div>

          <!-- 실제 오디오 엘리먼트 -->
          <audio
            :src="music.audio_url"
            :ref="(el) => (audioRefs[music.id] = el)"
            @timeupdate="onTimeUpdate(music.id, $event)"
            @loadedmetadata="onLoadedMetadata(music.id, $event)"
            class="audio-element"
          ></audio>

          <div class="controls">
            <!-- 재생/일시정지 버튼 -->
            <button class="play-btn" @click="togglePlay(music.id)">
              <span
                v-if="playingId === music.id && !audioRefs[music.id]?.paused"
                >⏸</span
              >
              <span v-else>▶</span>
            </button>

            <!-- 좋아요/싫어요 -->
            <button @click="vote(music.id, 'up')">
              👍 {{ music.upvotes }}
            </button>
            <button @click="vote(music.id, 'down')">
              👎 {{ music.downvotes }}
            </button>

            <!-- 다운로드 (로그인된 사용자만) -->
            <a
              v-if="isLoggedIn"
              :href="music.audio_url"
              download
              class="download-btn"
              >📥</a
            >
          </div>

          <!-- 진행 바 -->
          <div class="time">
            <div
              class="elapsed"
              :style="{ width: playProgress(music) + '%' }"
            ></div>
          </div>
          <p class="timetext time_now">
            {{ formatTime(currentTime[music.id] || 0) }}
          </p>
          <p class="timetext time_full">
            {{ formatTime(duration[music.id] || 0) }}
          </p>
        </div>
      </section>

      <!-- 댓글 섹션 -->
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
import { ref, reactive, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const auth = useAuthStore();
const route = useRoute();
const book = ref(null);
const emotionTags = ref([]);
const selectedTag = ref(null);

// <audio> DOM 참조 저장용
const audioRefs = reactive({});
const playingId = ref(null);
const currentTime = reactive({});
const duration = reactive({});

const isLoggedIn = computed(() => !!auth.token);

// 선택된 태그에 따라 필터링
const filteredMusics = computed(() => {
  if (!book.value?.musics) return [];
  return book.value.musics.filter(
    (m) => !selectedTag.value || m.tag === selectedTag.value
  );
});

// 재생 / 일시정지 토글
function togglePlay(id) {
  const audio = audioRefs[id];
  if (!audio) return;
  if (playingId.value && playingId.value !== id) {
    const prev = audioRefs[playingId.value];
    prev && !prev.paused && prev.pause();
  }
  if (audio.paused) {
    audio.play().catch((err) => console.error("play() failed:", err));
    playingId.value = id;
  } else {
    audio.pause();
  }
}

// 재생 위치 업데이트
function onTimeUpdate(id, e) {
  currentTime[id] = e.target.currentTime;
}
function onLoadedMetadata(id, e) {
  duration[id] = e.target.duration;
}

// 진행 바 퍼센트 계산
function playProgress(music) {
  const t = currentTime[music.id] || 0;
  const d = duration[music.id] || 1;
  return Math.floor((t / d) * 100);
}

// 시간 포맷 (m:ss)
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = String(Math.floor(sec % 60)).padStart(2, "0");
  return `${m}:${s}`;
}

// 상세 정보 불러오기
async function fetchBookDetail() {
  const res = await axios.get(`/api/books/${route.params.id}/`);
  book.value = res.data;
  if (book.value.musics.length && !selectedTag.value) {
    selectedTag.value = book.value.musics[0].tag;
  }
}
async function fetchEmotionTags() {
  const res = await axios.get("/api/emotion-tags/");
  emotionTags.value = res.data;
}

// 태그 선택
function selectTag(name) {
  selectedTag.value = name;
}

// 투표 로직 (생략 가능)
function vote(id, type) {
  // …기존 좋아요/싫어요 처리 로직…
}

onMounted(() => {
  Promise.all([fetchBookDetail(), fetchEmotionTags()]);
});
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
.author-info {
  display: flex;
  align-items: flex-start;
  background-color: #1e1e1e;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 2rem;
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
.tags {
  margin-top: 2rem;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
}
.tag {
  background: #666;
  padding: 0.3rem 0.6rem;
  margin: 0.2rem;
  border-radius: 0.5rem;
  cursor: pointer;
}
.tag.selected {
  background: linear-gradient(to right, #c210e6, #f03482, #ff7eb3);
}
.comments {
  margin-top: 2rem;
}
.comment-box {
  background: linear-gradient(to right, #ff758c, #ff7eb3);
  padding: 1rem;
  border-radius: 1rem;
}
/* ——————— Spotify 스타일 카드 ——————— */
.music {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}
.card {
  position: relative;
  width: 260px;
  height: 130px;
  background: linear-gradient(to right, #5807a3, #4563eb, #6f80e0, #dbd194);
  border-radius: 10px;
  padding: 10px;
}
.top {
  display: flex;
  gap: 10px;
}
.pfp {
  width: 40px;
  height: 40px;
  background-color: #333;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.texts {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.title-1 {
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin: 0;
}
.title-2 {
  color: rgb(255, 255, 255);
  font-size: 12px;
  margin: 0;
}
.playing {
  display: flex;
  justify-content: center;
  gap: 1px;
  width: 30px;
  height: 20px;
}
.greenline {
  background-color: #f0ff67;
  width: 2px;
  animation: playing 1s ease-in-out infinite;
  transform-origin: bottom;
}
.line-1 {
  animation-delay: 0s;
}
.line-2 {
  animation-delay: 0.2s;
}
.line-3 {
  animation-delay: 0.4s;
}
.line-4 {
  animation-delay: 0.6s;
}
.line-5 {
  animation-delay: 0.8s;
}
@keyframes playing {
  0% {
    transform: scaleY(0.2);
  }
  50% {
    transform: scaleY(1);
  }
  100% {
    transform: scaleY(0.2);
  }
}
.controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}
.play-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}
.download-btn {
  margin-left: auto;
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
}
.time {
  position: relative;
  width: 100%;
  height: 6px;
  background: #5e5e5e;
  border-radius: 3px;
  margin-top: 8px;
}
.elapsed {
  height: 100%;
  background: #ffffff;
  border-radius: 3px;
  transition: width 0.1s linear;
}
.timetext {
  position: absolute;
  font-size: 12px;
  color: rgb(255, 255, 255);
}
.time_now {
  bottom: -10px;
  left: 2;
}
.time_full {
  bottom: -10px;
  right: 0;
  padding-right: 10px;
}
</style>
