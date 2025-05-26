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

      <!-- 리뷰 섹션 -->
      <div class="card">
        <span class="title">{{ reviews.length }}건의 감상평이 있습니다.</span>

        <div v-for="review in reviews" :key="review.id" class="review">
          <div class="user-row">
            <img
              :src="review.user_avatar || '/default-avatar.png'"
              alt="프로필"
              class="avatar"
            />
            <!-- 내용 -->
            <div class="review-content">
              <div class="review-info">
                <strong>{{ review.user }}</strong>
                <span class="time">{{ formatDate(review.created_at) }}</span>
              </div>

              <div v-if="editingId === review.id">
                <textarea
                  v-model="editedContent"
                  rows="3"
                  class="edit-textarea"
                ></textarea>
                <div class="edit-buttons">
                  <button @click="updateReview(review.id)">저장</button>
                  <button @click="cancelEdit">취소</button>
                </div>
              </div>

              <p v-else>{{ review.content }}</p>
            </div>

            <!-- 오른쪽 상단 수정/삭제 -->
            <div
              v-if="review.user === currentUser"
              class="review-controls right"
            >
              <button @click="editReview(review)">수정</button>
              <button @click="deleteReview(review.id)">삭제</button>
            </div>
          </div>
        </div>

        <!-- 리뷰 입력창 -->
        <div v-if="isLoggedIn">
          <textarea
            v-model="newContent"
            placeholder="감상평을 남겨보세요..."
          ></textarea>
          <div class="formatting">
            <button @click="submitReview" class="submit-btn">➤</button>
          </div>
        </div>
        <div v-else class="login-prompt">
          <p>리뷰 작성은 로그인 후 가능합니다.</p>
          <button @click="alert('로그인이 필요한 활동입니다.')">➤</button>
        </div>
      </div>
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
const content = ref("");
const token = localStorage.getItem("token");

// <audio> DOM 참조 저장용
const audioRefs = reactive({});
const playingId = ref(null);
const currentTime = reactive({});
const duration = reactive({});
const isLoggedIn = computed(() => !!auth.token);

// 리뷰 기능
const currentUser = localStorage.getItem("nickname") || "익명";
const reviews = ref([]);
const newContent = ref("");
const editingId = ref(null);
const editedContent = ref("");

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

const fetchReviews = async () => {
  const { data } = await axios.get(`/api/reviews/?book=${route.params.id}`);
  reviews.value = data;
};

const submitReview = async () => {
  if (!newContent.value.trim()) return;
  await axios.post(
    "/api/reviews/",
    {
      book: route.params.id,
      content: newContent.value,
    },
    {
      headers: { Authorization: `Token ${token}` },
    }
  );
  newContent.value = "";
  fetchReviews();
};

const deleteReview = async (id) => {
  await axios.delete(`/api/reviews/${id}/`, {
    headers: { Authorization: `Token ${token}` },
  });
  fetchReviews();
};

const editReview = (review) => {
  editingId.value = review.id;
  editedContent.value = review.content;
};

const cancelEdit = () => {
  editingId.value = null;
  editedContent.value = "";
};

const updateReview = async (id) => {
  if (!editedContent.value.trim()) return;
  await axios.patch(
    `/api/reviews/${id}/`,
    {
      content: editedContent.value,
    },
    {
      headers: { Authorization: `Token ${token}` },
    }
  );
  editingId.value = null;
  editedContent.value = "";
  fetchReviews();
};

const formatDate = (iso) => {
  const date = new Date(iso);
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
};

onMounted(() => {
  Promise.all([fetchBookDetail(), fetchEmotionTags(), fetchReviews()]);
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
  margin-bottom: 2rem; /* 음악과 리뷰 사이 공간 */
}
.card {
  max-width: 1000px; /* 기존보다 넓게 */
  width: 100%;
  margin: 2rem auto;
  margin-top: 2rem;
  background: linear-gradient(to right, #c084f5, #f9e58e);
  padding: 1rem;
  border-radius: 1rem;
  color: black;
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

.card {
  background: linear-gradient(to right, #c084f5, #f9e58e);
  padding: 1rem;
  border-radius: 1rem;
  color: black;
  /* 이미 되어 있음 */
  display: flex;
  flex-direction: column;
}
.title {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}
.review {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}
.user-row {
  display: flex;
  align-items: flex-start;
  width: 100%;
  position: relative;
}
.review-controls.right {
  margin-left: auto;
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
  position: absolute;
  top: 0;
  right: 0;
}
.review-controls.right button {
  font-size: 0.75rem;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}
.review-controls.right button:hover {
  color: black;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 0.8rem;
}
.review-content {
  flex-grow: 1;
  max-width: 85%;
  background: #fff;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  flex: 1;
  word-wrap: break-word;
  white-space: pre-line; /* 줄바꿈 반영 */
}
.review-info {
  font-size: 0.8rem;
  color: gray;
  margin-bottom: 0.2rem;
}
.review-controls {
  display: flex;
  flex-direction: column;
  margin-left: 0.5rem;
}
.review-controls button,
.edit-buttons button {
  justify-content: flex-end;
  background: none;
  border: none;
  color: #444;
  font-size: 0.8rem;
  margin: 0.2rem 0;
  cursor: pointer;
}
.review-controls button:hover,
.edit-buttons button:hover {
  color: #000;
}
textarea {
  width: 100%;
  border: none;
  border-radius: 10px;
  margin-top: 1rem;
  padding: 1rem;
  font-size: 1rem;
  background-color: rgba(255, 255, 255, 0.4);
}
.formatting {
  display: flex;
  justify-content: flex-end;
}
.submit-btn {
  border: none;
  background: #805ad5;
  color: white;
  padding: 0.6rem 1rem;
  font-size: 1.2rem;
  border-radius: 50%;
  cursor: pointer;
  margin-top: 0.5rem;
}
</style>
