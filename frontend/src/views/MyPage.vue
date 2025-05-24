<template>
  <div class="my-page">
    <section class="profile-card">
      <img :src="currentAvatar" alt="avatar" class="avatar" />
      <div class="info">
        <div class="top-row">
          <h1>{{ profileStore.nickname || '닉네임 없음' }}</h1>
          <p>
            {{ userStore.user?.username || '아이디 없음' }} /
            {{ profileStore.age ?? '비공개' }}
          </p>
          <button @click="saveProfile" class="edit-btn">내 정보 수정하기</button>
        </div>

        <textarea v-model="editMessage" class="message-box" placeholder="나의 한마디를 작성할 수 있습니다."></textarea>

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

const currentAvatar = computed(() => {
  if (profileStore.avatarUrl) return profileStore.avatarUrl;
  return `/avatars/${profileStore.defaultAvatar || 'default1'}.png`;
});

function toggleTag(tag) {
  if (editedTags.value.includes(tag)) {
    editedTags.value = editedTags.value.filter((t) => t !== tag);
  } else {
    editedTags.value.push(tag);
  }
}

async function onFileChange(e) {
  avatarFile.value = e.target.files[0];
}

async function saveProfile() {
  const payload = {
    status_message: editMessage.value,
    emotion_tags: editedTags.value,
    default_avatar: editedDefaultAvatar.value,
  };
  if (avatarFile.value) payload.avatar = avatarFile.value;
  await profileStore.updateMe(payload);
  alert("프로필이 수정되었습니다.");
}

onMounted(async () => {
  if (!auth.user && auth.token) {
    await auth.fetchMe();
  }

  await profileStore.fetchMe();
  editMessage.value = profileStore.statusMessage;
  editedTags.value = [...profileStore.emotionTags];
  editedDefaultAvatar.value = profileStore.defaultAvatar;
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
  height: 160px;
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

</style>
