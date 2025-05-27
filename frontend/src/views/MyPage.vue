<template>
  <div class="my-page">
    <!-- 프로필 섹션 -->
    <section class="profile-card">
      <div class="profile-container">
        <!-- 보기 모드 -->
        <div v-if="!isEditing" class="view-mode">
          <div class="avatar-wrapper">
            <img :src="avatarUrl" alt="avatar" class="avatar" />
          </div>
          <div class="info-wrapper">
            <div class="info-header">
              <div class="title-group">
                <h1 class="nickname">
                  {{ profileStore.nickname || "나의 닉네임" }}
                </h1>
                <p class="sub-info">
                  {{ userStore.username || "나의 아이디" }}
                  <span>／</span>
                  {{ profileStore.age ?? "나이 비공개" }}
                </p>
              </div>
              <button @click="startEdit" class="edit-btn">
                내 정보 수정하기
              </button>
            </div>
            <p class="message-box view-mode">
              {{
                profileStore.statusMessage ||
                "나의 한마디를 작성할 수 있습니다."
              }}
            </p>
            <p class="tag-label">내가 선택한 태그</p>
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

        <!-- 편집 모드 -->
        <div v-else class="edit-mode">
          <div class="avatar-selection">
            <p class="avatar-label">기본 프로필 이미지 선택</p>
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
          <div class="edit-fields">
            <input
              v-model="editNickname"
              placeholder="닉네임"
              class="edit-input"
            />
            <textarea
              v-model="editMessage"
              class="message-box"
              placeholder="나의 한마디를 작성할 수 있습니다."
            />
            <p class="tag-label">태그 선택</p>
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
        </div>
      </div>
    </section>

    <!-- 내가 찜한 도서 섹션 -->
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

    <!-- 나의 리브리아 섹션 -->
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

const avatarUrl = computed(
  () =>
    profileStore.avatar_url ||
    `/avatars/${profileStore.defaultAvatar || "default1"}.png`
);

function startEdit() {
  editNickname.value = profileStore.nickname;
  editMessage.value = profileStore.statusMessage;
  editedTags.value = [...profileStore.emotionTags];
  editedDefaultAvatar.value = profileStore.defaultAvatar || "default1";
  isEditing.value = true;
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
  if (auth.user) userStore.setUserData(auth.user);
});
</script>

<style scoped>
.my-page {
  padding: 2rem;
  background: transparent;
  color: white;
}

/* 프로필 영역 */
.profile-card {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}
.profile-container {
  display: flex;
  width: 100%;
  max-width: 800px;
  gap: 2rem;
}

/* 보기 모드 */
.view-mode {
  display: flex;
  gap: 2rem;
  width: 100%;
}
.avatar-wrapper {
  flex-shrink: 0;
}
.avatar {
  width: 200px;
  margin-top: 30px;
  aspect-ratio: 1/1;
  border-radius: 50%;
  object-fit: cover;
  border: #e7e7e717 solid;
}
.info-wrapper {
  flex: 1;
}
.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title-group {
  display: flex;
  flex-direction: column;
}
.nickname {
  margin: 0;
}
.sub-info {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #aaa;
}
.sub-info span {
  margin: 0 0.4rem;
  color: #888;
}
.edit-btn {
  background: none;
  border: 1px solid #888;
  padding: 0.3rem 1rem;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  font-size: 0.9rem;
}

.message-box.view-mode {
  background: #222;
  border-radius: 8px;
  padding: 0.75rem;
  min-height: 60px;
  margin: 1rem 0;
  line-height: 1.4;
}

.tag-label {
  margin: 0.5rem 0 0.25rem;
  color: #aaa;
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
  padding: 0.35rem 0.8rem;
  border-radius: 16px;
  font-size: 0.85rem;
}
.tags button.selected {
  background: #b388f0;
}

/* 편집 모드 */
.edit-mode {
  display: flex;
  gap: 2rem;
  width: 100%;
}
.avatar-selection {
  width: 160px;
}
.avatar-label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  white-space: nowrap;
}
.avatar-options {
  display: flex;
  flex-direction: column;
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
.edit-fields {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 100px; /* ↑ 이 값을 3rem으로 올려서 “저장/취소” 버튼이 아바타 옵션 중앙 아래쯤 위치하도록 조정했습니다 */
}
.edit-input,
textarea {
  background: #222;
  color: #fff;
  border: none;
  padding: 0.4rem;
  margin-bottom: 20px;
  border-radius: 8px;
}
.edit-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

/* 책 섹션 */
.book-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
  padding: 0 1rem;
}
.section-header,
.book-list {
  max-width: 800px;
  width: 100%;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.section-header h2 {
  font-size: 1.2rem;
  margin: 0;
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
  justify-content: flex-start;
  overflow-x: auto;
  padding-bottom: 1rem;
}
.book-list::-webkit-scrollbar {
  height: 6px;
}
.book-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}
.book-card {
  flex: 0 0 auto;
  width: 130px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  background: #222;
  padding-left: 1px;
  padding-right: 1px;
  padding-top: 2px;
  border-radius: 10px;
}
.book-card img {
  width: 120px;
  height: 170px;
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
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.empty {
  color: #777;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>
