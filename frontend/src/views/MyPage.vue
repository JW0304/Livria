<template>
  <div class="my-page">
    <!-- 헤더 생략 -->

    <section class="profile-card">
      <img :src="currentAvatar" alt="avatar" class="avatar" />
      <div class="info">
        <h1>{{ profileStore.nickname }}</h1>
        <p>ID: {{ userStore.user.username }}, 나이: {{ profileStore.age }}</p>

        <!-- 한마디 -->
        <textarea v-model="editMessage"></textarea>

        <!-- 업로드 & 기본 선택 -->
        <div class="avatar-options">
          <label>
            업로드:
            <input type="file" @change="onFileChange" />
          </label>
          <label v-for="opt in avatarChoices" :key="opt[0]">
            <input
              type="radio"
              name="defaultAvatar"
              :value="opt[0]"
              v-model="editedDefaultAvatar"
            />
            {{ opt[1] }}
          </label>
        </div>

        <!-- 감성 태그 -->
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

        <button @click="saveProfile">내 정보 수정하기</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useProfileStore } from "@/stores/profile";
// import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const profileStore = useProfileStore();
const userStore = useUserStore();

// 로컬 편집용
const editMessage = ref("");
const editedTags = ref([]);
const editedDefaultAvatar = ref("");
const avatarFile = ref(null);

// 임의 태그 목록
const allTags = [
  "슬픔과 외로움",
  "사랑과 그리움",
  "위로와 평안",
  "에너지와 고조",
  "몽환적이고 감성적인",
];
// 기본 아바타 선택지 (서버와 동일 순서)
const avatarChoices = [
  ["default1", "기본 1"],
  ["default2", "기본 2"],
  ["default3", "기본 3"],
];

const currentAvatar = computed(() => {
  // 업로드된 URL 우선, 없으면 defaultAvatar 선택
  if (profileStore.avatarUrl) return profileStore.avatarUrl;
  return `/avatars/${profileStore.defaultAvatar}.png`;
});

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
  await profileStore.fetchMe();
  editMessage.value = profileStore.statusMessage;
  editedTags.value = [...profileStore.emotionTags];
  editedDefaultAvatar.value = profileStore.defaultAvatar;
});
</script>

<style scoped>
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}
.avatar-options {
  margin: 1rem 0;
}
</style>
