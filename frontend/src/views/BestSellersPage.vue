<template>
  <div class="best-sellers-page">
    <h1>베스트셀러</h1>
    <div
      v-for="book in books"
      :key="book.id"
      class="book-card"
      @click="goToDetail(book.id)"
    >
      <img :src="book.cover_url" alt="책 이미지" class="book-image" />

      <div class="book-info">
        <h2 class="book-title">{{ book.title }}</h2>
        <p class="book-author">작가: {{ book.author_name }}</p>
        <p class="book-pub">
          출판사: {{ book.publisher }}<br />
          출판일: {{ book.pub_date }}
        </p>

        <!-- 태그 리스트 -->
        <div class="tags">
          <span
            v-for="tag in book.tags"
            :key="tag"
            class="tag"
            :class="{ selected: selectedTags[book.id] === tag }"
            @click.stop="selectTag(book.id, tag)"
            >{{ tag }}</span
          >
        </div>

        <!-- 오디오 컨트롤 -->
        <div class="audio-controls">
          <audio
            :src="getAudioUrl(book, selectedTags[book.id])"
            :ref="(el) => (audioRefs[book.id] = el)"
            @timeupdate="onTimeUpdate(book.id, $event)"
            @loadedmetadata="onLoadedMetadata(book.id, $event)"
            class="audio-element"
          ></audio>

          <button class="play-btn" @click.stop="togglePlay(book.id)">
            <span v-if="playingId === book.id && !audioRefs[book.id]?.paused"
              >⏸</span
            ><span v-else>▶</span>
          </button>

          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: playProgress(book.id) + '%' }"
            ></div>
          </div>

          <p class="progress-text">
            {{ formatTime(currentTime[book.id] || 0) }} /
            {{ formatTime(duration[book.id] || 0) }}
          </p>

          <a
            v-if="isLoggedIn"
            :href="getAudioUrl(book, selectedTags[book.id])"
            download
            class="download-btn"
            >⬇️</a
          >
        </div>

        <div class="icons">
          <span class="icon">♡</span>
          <span class="icon">👜</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();
const isLoggedIn = computed(() => !!auth.token);

const books = ref([]);
const selectedTags = reactive({});
const audioRefs = reactive({});
const playingId = ref(null);
const currentTime = reactive({});
const duration = reactive({});

function goToDetail(id) {
  router.push({ name: "BookDetail", params: { id } });
}

async function fetchBooks() {
  const { data } = await axios.get("/api/books/?category=1");
  books.value = data.map((book) => {
    const tags = book.musics.map((m) => m.tag);
    selectedTags[book.id] = "사랑과 그리움";
    return { ...book, tags };
  });
}

onMounted(fetchBooks);

function selectTag(bookId, tag) {
  if (selectedTags[bookId] === tag) return;
  if (playingId.value === bookId) {
    audioRefs[bookId]?.pause();
    playingId.value = null;
  }
  selectedTags[bookId] = tag;
  currentTime[bookId] = 0;
  duration[bookId] = 0;
}

function getAudioUrl(book, tag) {
  const m = book.musics.find((x) => x.tag === tag);
  return m?.audio_url || "";
}

function togglePlay(bookId) {
  const audio = audioRefs[bookId];
  if (!audio) return;
  if (playingId.value && playingId.value !== bookId) {
    audioRefs[playingId.value]?.pause();
  }
  if (audio.paused) {
    audio.play().catch(console.error);
    playingId.value = bookId;
  } else {
    audio.pause();
  }
}

function onTimeUpdate(bookId, e) {
  currentTime[bookId] = e.target.currentTime;
}
function onLoadedMetadata(bookId, e) {
  duration[bookId] = e.target.duration;
}
function playProgress(bookId) {
  const t = currentTime[bookId] || 0;
  const d = duration[bookId] || 1;
  return Math.floor((t / d) * 100);
}
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = String(Math.floor(sec % 60)).padStart(2, "0");
  return `${m}:${s}`;
}
</script>

<style scoped>
.best-sellers-page {
  padding: 2rem;
  background: #000;
  color: #fff;
}
.book-card {
  display: flex;
  gap: 1.5rem;
  padding: 1rem;
  margin-bottom: 2rem;
  border: 1px solid #444;
  border-radius: 8px;
  cursor: pointer;
}
.book-image {
  width: 160px;
  height: 220px;
  object-fit: cover;
  border-radius: 4px;
  background: #333;
}
.book-info {
  flex: 1;
}
.book-title {
  font-size: 1.8rem;
  margin-bottom: 0.3rem;
}
.book-author,
.book-pub {
  margin: 0.2rem 0;
  font-size: 1rem;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0.5rem 0;
}
.tag {
  background: #222;
  border: 1px solid #555;
  padding: 0.3rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  cursor: pointer;
  color: #fff;
}
.tag.selected {
  background: linear-gradient(to right, #5807a3, #4563eb, #6f80e0, #dbd194);
  border-color: #ffffff;
}
.audio-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.8rem 0;
}
.audio-element {
  display: none;
}
.play-btn,
.download-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
}
.progress-bar {
  flex: 1;
  height: 6px;
  background: #444;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #c210e6, #f03482, #ff7eb3);
  width: 0%;
  transition: width 0.1s linear;
}
.progress-text {
  font-size: 0.8rem;
  color: #ccc;
  margin-left: 0.5rem;
}
.icons {
  display: flex;
  gap: 1rem;
  font-size: 1.2rem;
  margin-top: 0.5rem;
}
</style>
