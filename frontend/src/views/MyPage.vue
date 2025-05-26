<template>
  <div class="my-page">
    <section class="profile-card">
      <!-- 편집 모드 -->
      <div v-if="isEditing" class="edit-mode">
        <div class="avatar-selection">
          <p>기본 프로필 이미지 선택</p>
          <div class="avatar-options">
            <div
              v-for="[filename, label] in avatarChoices"
              :key="filename"
              class="avatar-option"
            >
              <img
                :src="`/avatars/${filename}.png`"
                :class="{ selected: editedDefaultAvatar === filename }"
                @click="editedDefaultAvatar = filename"
              />
              <p>{{ label }}</p>
            </div>
          </div>
        </div>

        <input v-model="editNickname" placeholder="닉네임" class="edit-input" />
        <textarea
          v-model="editMessage"
          class="message-box"
          placeholder="나의 한마디를 작성할 수 있습니다."
        ></textarea>

        <div class="tags">
          <button
            v-for="tag in allTags"
            :key="tag"
            :class="{ selected: editedTags.includes(tag) }"
            @click="toggleTag(tag)"
          >
            {{ tag }}
          </button>
        </div>

        <div class="edit-actions">
          <button @click="saveProfile" class="edit-btn">저장</button>
          <button @click="cancelEdit" class="edit-btn">취소</button>
        </div>
      </div>

      <!-- 보기 모드 -->
      <div v-else>
        <img :src="avatarUrl" alt="avatar" class="avatar" />

        <div class="info">
          <div class="top-row">
            <h1>{{ profileStore.nickname || "나의 닉네임" }}</h1>
            <p>
              {{ userStore.username || "나의 아이디" }} /
              {{ profileStore.age ?? "나이 비공개" }}
            </p>
            <button @click="startEdit" class="edit-btn">
              내 정보 수정하기
            </button>
          </div>

          <p class="message-box">
            {{
              profileStore.statusMessage || "나의 한마디를 작성할 수 있습니다."
            }}
          </p>

          <p color="lightgray">내가 선택한 태그</p>
          <div class="tags">
            <button
              v-for="tag in profileStore.emotionTags"
              :key="tag"
              class="selected"
              disabled
            >
              {{ tag }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 내가 찜한 도서 -->
    <section class="book-section">
      <div class="section-header">
        <h2>내가 찜한 도서</h2>
        <RouterLink to="/favorites" class="more-link">더보기</RouterLink>
      </div>
      <div class="book-list">
        <RouterLink
          v-for="book in profileStore.favorites"
          :key="book.id"
          :to="`/books/${book.id}`"
          class="book-card"
        >
          <img :src="book.cover_url" alt="cover" />
          <p class="book-title">{{ book.title }}</p>
          <p class="book-author">{{ book.author_name }}</p>
        </RouterLink>
        <div v-if="!profileStore.favorites.length" class="empty">
          찜한 도서가 없습니다.
        </div>
      </div>
    </section>

    <!-- 나의 리브리아 -->
    <section class="book-section">
      <div class="section-header">
        <h2>나의 리브리아</h2>
        <RouterLink to="/read-history" class="more-link">더보기</RouterLink>
      </div>
      <div class="book-list">
        <RouterLink
          v-for="book in profileStore.readBooks"
          :key="book.id"
          :to="`/books/${book.id}`"
          class="book-card"
        >
          <img :src="book.cover_url" alt="cover" />
          <p class="book-title">{{ book.title }}</p>
          <p class="book-author">{{ book.author_name }}</p>
        </RouterLink>
        <div v-if="!profileStore.readBooks.length" class="empty">
          읽은 도서가 없습니다.
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useProfileStore } from "@/stores/profile";
import { useUserStore } from "@/stores/user";
import { useAuthStore } from "@/stores/auth";

const profileStore = useProfileStore();
const userStore = useUserStore();
const auth = useAuthStore();

const isEditing = ref(false);
const editNickname = ref("");
const editMessage = ref("");
const editedTags = ref([]);
const editedDefaultAvatar = ref("");

const allTags = [
  "슬픔과 외로움",
  "사랑과 그리움",
  "위로와 평안",
  "에너지와 고조",
  "몽환적이고 감성적인",
];
const avatarChoices = [
  ["default1", "기본 1"],
  ["default2", "기본 2"],
  ["default3", "기본 3"],
];

// 프로필 스토어에서 내려주는 full URL 우선, 없으면 public/avatars 에서 기본 선택지 로드
const avatarUrl = computed(() => {
  return (
    profileStore.avatar_url ||
    `/avatars/${profileStore.defaultAvatar || "default1"}.png`
  );
});

function startEdit() {
  isEditing.value = true;
  editNickname.value = profileStore.nickname;
  editMessage.value = profileStore.statusMessage;
  editedTags.value = [...profileStore.emotionTags];
  editedDefaultAvatar.value = profileStore.defaultAvatar || "default1";
}
function cancelEdit() {
  isEditing.value = false;
}

function toggleTag(tag) {
  if (editedTags.value.includes(tag)) {
    editedTags.value = editedTags.value.filter((t) => t !== tag);
  } else {
    editedTags.value.push(tag);
  }
}

async function saveProfile() {
  const payload = {
    nickname: editNickname.value,
    status_message: editMessage.value,
    emotion_tags: editedTags.value,
    default_avatar: editedDefaultAvatar.value,
  };
  try {
    await profileStore.updateMe(payload);
    await profileStore.fetchMe();
    isEditing.value = false;
    alert("프로필이 수정되었습니다.");
  } catch {
    alert("프로필 수정에 실패했습니다.");
  }
}

onMounted(async () => {
  await profileStore.fetchMe();
  if (auth.user) {
    userStore.setUserData(auth.user);
  }
});
</script>

<style scoped>
.my-page {
  color: #fff;
  padding: 2rem;
}
.profile-card {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
}
.avatar {
  width: 160px;
  aspect-ratio: 1/1;
  border-radius: 50%;
  background: #444;
  object-fit: cover;
}
.info {
  flex: 1;
}
.top-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}
.message-box {
  width: 100%;
  height: 60px;
  margin: 1rem 0;
  background: #222;
  border: none;
  border-radius: 8px;
  color: #fff;
  padding: 0.5rem;
}
.edit-btn {
  margin-left: auto;
  background: none;
  border: 1px solid #888;
  padding: 0.3rem 1rem;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.tags button {
  background: #555;
  color: #fff;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  cursor: pointer;
}
.tags button.selected {
  background: #b388f0;
}

.book-section {
  margin-top: 2rem;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.section-header h2 {
  font-size: 1.2rem;
}
.more-link {
  font-size: 0.9rem;
  color: #aaa;
  text-decoration: underline;
}
.book-list {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.book-card {
  display: block;
  width: 100px;
  text-align: center;
  color: inherit;
  text-decoration: none;
}
.book-card img {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 4px;
}
.book-title {
  font-size: 0.9rem;
  margin: 0.3rem 0 0.1rem;
}
.book-author {
  font-size: 0.75rem;
  color: #ccc;
}
.empty {
  color: #777;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.avatar-selection {
  margin-bottom: 1rem;
}
.avatar-options {
  display: flex;
  gap: 0.5rem;
}
.avatar-option {
  text-align: center;
}
.avatar-option img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  cursor: pointer;
}
.avatar-option img.selected {
  border-color: #b388f0;
}
.avatar-option p {
  margin-top: 0.3rem;
  font-size: 0.8rem;
  color: #ccc;
}
.edit-input {
  background: #222;
  color: #fff;
  border: none;
  padding: 0.4rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  width: 100%;
}
.edit-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
