<template>
  <div class="favorites-page">
    <h2>당신의 아리아</h2>

    <!-- 찜한 도서가 없을 때 -->
    <div v-if="favorites.length === 0" class="empty-message">
      <p>아직 선율이 도착하지 않았습니다.</p>
    </div>

    <!-- 찜한 도서가 있을 때 -->
    <div v-else>
      <div v-for="book in favorites" :key="book.id" class="book-card">
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
              v-for="tag in book.musics.map((m) => m.tag)"
              :key="tag"
              class="tag"
              :class="{ selected: selectedTags[book.id] === tag }"
              @click.stop="selectTag(book.id, tag)"
            >
              {{ tag }}
            </span>
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

          <!-- 읽음·찜 토글 -->
          <div class="icons">
            <!-- 읽음(하트) -->
            <span
              class="icon favorite"
              :class="{ active: readSet.has(book.id) }"
              @click.stop="toggleRead(book.id)"
            >
              {{ readSet.has(book.id) ? "❤️ 읽음" : "🤍 읽기" }}
            </span>
            <!-- 찜(가방) -->
            <span
              class="icon wish"
              :class="{ active: wishSet.has(book.id) }"
              @click.stop="toggleWish(book.id)"
            >
              {{ wishSet.has(book.id) ? "🛍️ 찜취소" : "👜 찜하기" }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const isLoggedIn = computed(() => !!auth.token);

// 찜한 도서 데이터
const favorites = ref([]);
// 각 도서별 선택된 태그 초기화용
const selectedTags = reactive({});
// 오디오 컨트롤 참조
const audioRefs = reactive({});
const playingId = ref(null);
const currentTime = reactive({});
const duration = reactive({});

// 읽음·찜 상태 추적용 Set
const readSet = ref(new Set());
const wishSet = ref(new Set());

// 페이지 로드시 찜한 도서 불러오기
onMounted(async () => {
  try {
    // 1) 찜한 도서 목록
    const resp = await axios.get("/api/auth/users/me/favorites");
    favorites.value = resp.data;

    // 2) 각 도서 태그 초기화
    favorites.value.forEach((book) => {
      const tags = book.musics.map((m) => m.tag);
      selectedTags[book.id] = tags[0] || "";
    });

    // 3) 로그인 상태면 읽음·찜 초기값 불러오기
    if (isLoggedIn.value) {
      const me = await axios.get("/api/auth/users/me");
      me.data.read_books.forEach((b) => readSet.value.add(b.id));
      me.data.favorites.forEach((b) => wishSet.value.add(b.id));
    }
  } catch (e) {
    console.error("찜한 도서 목록 로딩 실패", e);
  }
});

function selectTag(bookId, tag) {
  if (selectedTags[bookId] === tag) return;
  audioRefs[bookId]?.pause();
  playingId.value = null;
  selectedTags[bookId] = tag;
  currentTime[bookId] = 0;
  duration[bookId] = 0;
}

function getAudioUrl(book, tag) {
  const mus = Array.isArray(book.musics) ? book.musics : [];
  const m = mus.find((x) => x.tag === tag);
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

// 읽음(리스트) 토글
async function toggleRead(bookId) {
  if (!isLoggedIn.value) return alert("로그인이 필요합니다.");
  try {
    if (readSet.value.has(bookId)) {
      await axios.delete(`/api/auth/users/me/read_books/${bookId}`);
      readSet.value.delete(bookId);
    } else {
      await axios.post(`/api/auth/users/me/read_books/${bookId}`);
      readSet.value.add(bookId);
    }
  } catch (e) {
    console.error(e);
  }
}

// 찜(wish) 토글
async function toggleWish(bookId) {
  if (!isLoggedIn.value) return alert("로그인이 필요합니다.");
  try {
    if (wishSet.value.has(bookId)) {
      await axios.delete(`/api/auth/users/me/favorites/${bookId}`);
      wishSet.value.delete(bookId);
    } else {
      await axios.post(`/api/auth/users/me/favorites/${bookId}`);
      wishSet.value.add(bookId);
    }
  } catch (e) {
    console.error(e);
  }
}
</script>

<style scoped>
.favorites-page {
  padding: 2rem;
  background: transparent;
  color: white;
}
.empty-message p {
  font-size: 1.2rem;
  color: #888;
  font-style: italic;
}
.book-card {
  display: flex;
  gap: 1.5rem;
  padding: 1rem;
  margin-bottom: 2rem;
  border: 1px solid #444;
  border-radius: 8px;
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
  border-color: #fff;
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
.icon {
  cursor: pointer;
}
.icon.active {
  filter: drop-shadow(0 0 4px #ffeb3b);
}
</style>
