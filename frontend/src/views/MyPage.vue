<template>
  <div class="my-page">
    <section class="profile-card">
      <!-- 수정 모드일 때 -->
      <div v-if="isEditing" class="edit-mode">
        <div class="avatar-selection">
          <p>기본 프로필 이미지 선택</p>
          <div class="avatar-options">
            <img
              v-for="[filename, label] in avatarChoices"
              :key="filename"
              :src="`/avatars/${filename}.png`"
              :class="{ selected: editedDefaultAvatar === filename }"
              @click="editedDefaultAvatar = filename"
            />
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
          <button @click="isEditing = false" class="edit-btn">취소</button>
        </div>
      </div>

      <!-- 보기 모드일 때 -->
      <div v-else>
        <img :src="avatarUrl" alt="avatar" class="avatar" />

        <div class="info">
          <div class="top-row">
            <h1>{{ profileStore.nickname || "나의 닉네임" }}</h1>
            <p>
              {{ userStore.username || "나의 아이디" }} /
              {{ profileStore.age ?? "나이 비공개" }}
            </p>
            <button @click="isEditing = true" class="edit-btn">
              내 정보 수정하기
            </button>
          </div>

          <!-- 메시지 박스 -->
          <!-- <textarea v-model="editMessage" class="message-box" placeholder="나의 한마디를 작성할 수 있습니다."></textarea>
           -->

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

          <!-- 모든 태그 -->
          <!-- <div class="tags">
            <button
              v-for="tag in allTags"
              :key="tag"
              :class="{ selected: editedTags.includes(tag) }"
              @click="toggleTag(tag)"
            >
              {{ tag }}
            </button>
          </div> -->
        </div>
      </div>
    </section>

    <!-- 도서 섹션 -->
    <section class="book-section">
      <div class="section-header">
        <h2>내가 찜한 도서</h2>
        <RouterLink to="/favorites" class="more-link">더보기</RouterLink>
      </div>
      <div class="book-list">
        <div v-for="n in 3" :key="'favorite-' + n" class="book-placeholder" />
      </div>
    </section>

    <section class="book-section">
      <div class="section-header">
        <h2>나의 리브리아</h2>
        <RouterLink to="/read-history" class="more-link">더보기</RouterLink>
      </div>
      <div class="book-list">
        <div v-for="n in 4" :key="'library-' + n" class="book-placeholder" />
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
const avatarFile = ref(null);

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

// 안 씀, 아래를 씀 (avataUrl)
const currentAvatar = computed(() => {
  if (profileStore.avatarUrl) return profileStore.avatarUrl;
  return `/avatars/${profileStore.defaultAvatar || "default1"}.png`;
});

const avatarUrl = computed(() => {
  const defaultAvatar = auth.user?.default_avatar || "default1";
  return `/avatars/${defaultAvatar}.png`;
});

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
  // if (avatarFile.value) payload.avatar = avatarFile.value;
  await profileStore.updateMe(payload);
  await profileStore.fetchMe(); // 다시 갱신
  isEditing.value = false;
  alert("프로필이 수정되었습니다.");
}

async function onFileChange(e) {
  avatarFile.value = e.target.files[0];
}

onMounted(async () => {
  if (!auth.user && auth.token) {
    await auth.fetchMe();
  }

  await profileStore.fetchMe();

  // userStore에 username을 복사
  if (auth.user) {
    userStore.setUserData(auth.user);
  }

  editMessage.value = profileStore.statusMessage;
  editedTags.value = [...profileStore.emotionTags];
  editedDefaultAvatar.value = profileStore.defaultAvatar;
  editNickname.value = profileStore.nickname;
});
</script>

<style scoped>
.my-page {
  color: white;
  padding: 2rem;
}
.profile-card {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 3rem;
}
.avatar {
  width: 160px;
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  background-color: #444;
  object-fit: cover;
}
.info {
  flex-grow: 1;
}
.top-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.message-box {
  width: 100%;
  height: 60px;
  margin: 1rem 0;
  background: #222;
  border: none;
  border-radius: 8px;
  color: white;
  padding: 0.5rem;
}
.edit-btn {
  margin-left: auto;
  background: none;
  border: 1px solid #888;
  padding: 0.3rem 1rem;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.tags button {
  background: #555;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  cursor: pointer;
}
.tags button.selected {
  background-color: #b388f0;
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
.book-placeholder {
  width: 100px;
  height: 140px;
  background: #ddd;
  border-radius: 8px;
}

/* 추가된 스타일 */
.avatar-selection {
  margin-bottom: 1rem;
}
.avatar-options {
  display: flex;
  gap: 0.5rem;
}
.avatar-options img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  cursor: pointer;
}
.avatar-options img.selected {
  border-color: #b388f0;
}
.edit-input {
  background: #222;
  color: white;
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
