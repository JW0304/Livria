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
        <!-- 읽음/찜 토글 아이콘 -->
        <div class="icons">
          <span
            class="icon heart"
            :class="{ active: isInRead(book.id) }"
            @click.stop="toggleRead(book.id)"
          >
            {{ isInRead(book.id) ? "❤️ 읽음" : "♡ 읽기" }}
          </span>
          <span
            class="icon lock"
            :class="{ active: isInFav(book.id) }"
            @click.stop="toggleFavorite(book.id)"
          >
            {{ isInFav(book.id) ? "🔓 찜 취소" : "🔒 찜하기" }}
          </span>
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

          <audio
            :src="music.audio_url"
            :ref="(el) => (audioRefs[music.id] = el)"
            @timeupdate="onTimeUpdate(music.id, $event)"
            @loadedmetadata="onLoadedMetadata(music.id, $event)"
            class="audio-element"
          ></audio>

          <div class="controls">
            <button
              type="button"
              class="play-btn"
              @click="togglePlay(music.id)"
            >
              <span
                v-if="playingId === music.id && !audioRefs[music.id]?.paused"
                >⏸</span
              ><span v-else>▶</span>
            </button>

            <button
              type="button"
              class="like-btn"
              :class="{ liked: isLiked[music.id] }"
              @click="toggleLike(music.id)"
            >
              {{ isLiked[music.id] ? "👍 좋아요 취소" : "👍 좋아요" }}
            </button>

            <button
              type="button"
              class="dislike-btn"
              :class="{ disliked: isDisliked[music.id] }"
              @click="toggleDislike(music.id)"
            >
              {{ isDisliked[music.id] ? "👎 싫어요 취소" : "👎 싫어요" }}
            </button>

            <a
              v-if="isLoggedIn"
              :href="music.audio_url"
              download
              class="download-btn"
              >📥</a
            >
          </div>

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
              :src="review.user_avatar || '/avatars/default2.png'"
              alt="프로필"
              class="avatar"
            />
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
                  <button type="button" @click="updateReview(review.id)">
                    저장
                  </button>
                  <button type="button" @click="cancelEdit">취소</button>
                </div>
              </div>

              <p v-else>{{ review.content }}</p>
            </div>

            <div
              v-if="review.user === currentUser"
              class="review-controls right"
            >
              <button type="button" @click="editReview(review)">수정</button>
              <button type="button" @click="deleteReview(review.id)">
                삭제
              </button>
            </div>
          </div>
        </div>

        <div v-if="isLoggedIn" class="new-review">
          <textarea
            v-model="newContent"
            placeholder="감상평을 남겨보세요..."
            rows="3"
          ></textarea>
          <div class="formatting">
            <button type="button" @click="submitReview" class="submit-btn">
              ➤
            </button>
          </div>
        </div>
        <div v-else class="login-prompt">
          <p>리뷰 작성은 로그인 후 가능합니다.</p>
          <button type="button" @click="alert('로그인이 필요한 활동입니다.')">
            ➤
          </button>
        </div>
      </div>

      <!-- 추천 도서 섹션 -->
      <section class="similar-books" v-if="similarBooks.length">
        <h2>이 책과 유사한 도서</h2>
        <div class="card-list">
          <div
            v-for="sim in similarBooks"
            :key="sim.id"
            class="card similar-card"
            @click="goToBook(sim.id)"
          >
            <img :src="sim.cover_url" alt="cover" class="cover-small" />
            <p class="book-title">{{ sim.title }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useProfileStore } from "@/stores/profile";
import axios from "axios";

const auth = useAuthStore();
const profile = useProfileStore();
const route = useRoute();
const router = useRouter();

const book = ref(null);
const emotionTags = ref([]);
const selectedTag = ref(null);

const audioRefs = reactive({});
const playingId = ref(null);
const currentTime = reactive({});
const duration = reactive({});

const isLoggedIn = computed(() => !!auth.token);

const reviews = ref([]);
const newContent = ref("");
const editingId = ref(null);
const editedContent = ref("");

const isLiked = reactive({});
const isDisliked = reactive({});

const similarBooks = ref([]);

const currentUser = computed(() => auth.user?.username || "");

const readIds = computed(() => profile.readBooks.map((b) => b.id));
const favIds = computed(() => profile.favorites.map((b) => b.id));
const isInRead = (id) => readIds.value.includes(id);
const isInFav = (id) => favIds.value.includes(id);

function togglePlay(id) {
  const audio = audioRefs[id];
  if (!audio) return;
  if (playingId.value && playingId.value !== id)
    audioRefs[playingId.value]?.pause();
  if (audio.paused) {
    audio.play().catch(console.error);
    playingId.value = id;
  } else {
    audio.pause();
  }
}
function onTimeUpdate(id, e) {
  currentTime[id] = e.target.currentTime;
}
function onLoadedMetadata(id, e) {
  duration[id] = e.target.duration;
}
function playProgress(music) {
  const t = currentTime[music.id] || 0;
  const d = duration[music.id] || 1;
  return Math.floor((t / d) * 100);
}
function formatTime(sec) {
  const m = Math.floor(sec / 60),
    s = String(Math.floor(sec % 60)).padStart(2, "0");
  return `${m}:${s}`;
}
function formatDate(iso) {
  const d = new Date(iso);
  return `${d.toLocaleDateString()} ${d.toLocaleTimeString()}`;
}

async function toggleLike(musicId) {
  if (!auth.token) return;
  const payload = { is_like: !isLiked[musicId] };
  await axios.post(`/api/music/${musicId}/react/`, payload, {
    headers: { Authorization: `Token ${auth.token}` },
  });
  isLiked[musicId] = !isLiked[musicId];
  if (isLiked[musicId]) isDisliked[musicId] = false;
}
async function toggleDislike(musicId) {
  if (!auth.token) return;
  const payload = { is_like: isDisliked[musicId] };
  await axios.post(`/api/music/${musicId}/react/`, payload, {
    headers: { Authorization: `Token ${auth.token}` },
  });
  isDisliked[musicId] = !isDisliked[musicId];
  if (isDisliked[musicId]) isLiked[musicId] = false;
}

async function toggleRead(bookId) {
  if (!auth.token) return;
  if (isInRead(bookId))
    await axios.delete(`/api/auth/users/me/read_books/${bookId}`);
  else await axios.post(`/api/auth/users/me/read_books/${bookId}`);
  await profile.fetchMe();
}
async function toggleFavorite(bookId) {
  if (!auth.token) return;
  if (isInFav(bookId))
    await axios.delete(`/api/auth/users/me/favorites/${bookId}`);
  else await axios.post(`/api/auth/users/me/favorites/${bookId}`);
  await profile.fetchMe();
}

const filteredMusics = computed(
  () =>
    book.value?.musics?.filter(
      (m) => !selectedTag.value || m.tag === selectedTag.value
    ) || []
);
function selectTag(name) {
  selectedTag.value = name;
}

async function fetchBookDetail() {
  const { data } = await axios.get(`/api/books/${route.params.id}/`);
  book.value = data;
  if (data.musics?.length && !selectedTag.value)
    selectedTag.value = data.musics[0].tag;
}
async function fetchEmotionTags() {
  const { data } = await axios.get("/api/emotion-tags/");
  emotionTags.value = data;
}
async function fetchReviews() {
  const { data } = await axios.get(`/api/reviews/?book=${route.params.id}`);
  reviews.value = data;
}
async function fetchSimilarBooks() {
  const { data } = await axios.get(`/api/books/${route.params.id}/similar/`);
  similarBooks.value = data;
}

async function submitReview() {
  if (!newContent.value.trim()) return;
  await axios.post(
    "/api/reviews/",
    { book: route.params.id, content: newContent.value },
    { headers: { Authorization: `Token ${auth.token}` } }
  );
  newContent.value = "";
  await fetchReviews();
}
async function updateReview(id) {
  await axios.patch(
    `/api/reviews/${id}/`,
    { content: editedContent.value },
    { headers: { Authorization: `Token ${auth.token}` } }
  );
  editingId.value = null;
  editedContent.value = "";
  await fetchReviews();
}
async function deleteReview(id) {
  await axios.delete(`/api/reviews/${id}/`, {
    headers: { Authorization: `Token ${auth.token}` },
  });
  await fetchReviews();
}

function goToBook(id) {
  router.push({ name: "BookDetail", params: { id } });
}

watch(
  () => route.params.id,
  async () => {
    await Promise.all([
      fetchBookDetail(),
      fetchEmotionTags(),
      fetchReviews(),
      fetchSimilarBooks(),
    ]);
    if (auth.token) await profile.fetchMe();
  }
);

onMounted(async () => {
  await Promise.all([
    fetchBookDetail(),
    fetchEmotionTags(),
    fetchReviews(),
    fetchSimilarBooks(),
  ]);
  if (auth.token) await profile.fetchMe();

  const savedLikes = localStorage.getItem("liked");
  const savedDislikes = localStorage.getItem("disliked");
  if (savedLikes) Object.assign(isLiked, JSON.parse(savedLikes));
  if (savedDislikes) Object.assign(isDisliked, JSON.parse(savedDislikes));
});
</script>

<style scoped>
.book-detail {
  padding: 2rem;
  background: transparent;
  color: white;
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
  margin-left: auto;
  display: flex;
  gap: 1rem;
  align-items: center;
}
.icon {
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.1s, opacity 0.1s;
}
.icon.active {
  transform: scale(1.2);
  opacity: 0.7;
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
.music {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.card {
  max-width: 1000px;
  width: 100%;
  margin: 2rem auto;
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
  color: white;
  font-size: 12px;
  margin: 0;
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
  left: 2px;
}
.time_full {
  bottom: -10px;
  right: 0;
  padding-right: 10px;
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
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  gap: 0.3rem;
}
.review-controls.right button {
  background: none;
  border: none;
  color: #666;
  font-size: 0.8rem;
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
  object-fit: cover;
}
.review-content {
  flex-grow: 1;
  background: #fff;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  white-space: pre-line;
}
.review-info {
  font-size: 0.8rem;
  color: gray;
  margin-bottom: 0.2rem;
}
.textarea,
.edit-textarea {
  width: 100%;
  border: none;
  border-radius: 6px;
  padding: 0.5rem;
  margin-top: 0.5rem;
}
.edit-buttons,
.formatting {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.submit-btn {
  border: none;
  background: #805ad5;
  color: white;
  padding: 0.6rem 1rem;
  font-size: 1.2rem;
  border-radius: 50%;
  cursor: pointer;
}
.login-prompt {
  margin-top: 1rem;
  color: #ccc;
}
.liked {
  color: #ff6b6b;
}
.disliked {
  color: #6bafff;
}
.similar-books {
  margin-top: 2rem;
}
.similar-books h2 {
  color: white;
  margin-bottom: 1rem;
}
.card-list {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.similar-card {
  background: #333;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  width: 150px;
  text-align: center;
}
.cover-small {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 0.5rem;
}
.book-title {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: white;
}
</style>
