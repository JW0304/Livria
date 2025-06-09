<template>
  <div class="signup-wrapper">
    <div class="signup-box">
      <div class="brand">
        <img src="@/assets/purplelogo.png" alt="Livria 로고" class="logo" />
        <h1 class="brand-text">Livria</h1>
      </div>

      <form @submit.prevent="handleSignup">
        <input
          v-model="username"
          placeholder="아이디 (최대 30자)"
          maxlength="30"
          required
        />
        <input
          v-model="password"
          type="password"
          placeholder="비밀번호 (최대 30자)"
          maxlength="30"
          required
        />
        <input
          v-model="passwordCheck"
          type="password"
          placeholder="비밀번호 재입력"
          maxlength="30"
          required
        />
        <input
          v-model="nickname"
          placeholder="닉네임 (최대 30자)"
          maxlength="30"
          required
        />
        <input
          v-model.number="age"
          type="number"
          min="1"
          max="110"
          placeholder="나이 (1~110)"
          required
        />

        <div class="tags">
          <p class="tag-label">
            태그를 선택하세요 (1개 이상)<br />
            <small>* 태그를 기반으로 도서에 맞는 음악을 추천해드립니다.</small>
          </p>
          <div class="tag-list">
            <button
              v-for="tag in allTags"
              :key="tag"
              type="button"
              :class="{ selected: selectedTags.includes(tag) }"
              @click="toggleTag(tag)"
            >
              {{ tag }}
            </button>
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="!isValid">
          제출
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const auth = useAuthStore();
const router = useRouter();

const username = ref("");
const password = ref("");
const passwordCheck = ref("");
const nickname = ref("");
const age = ref(null);
const selectedTags = ref([]);

const allTags = [
  "슬픔과 외로움",
  "사랑과 그리움",
  "위로와 평안",
  "에너지와 고조",
  "몽환적이고 감성적인",
];

const toggleTag = (tag) => {
  if (selectedTags.value.includes(tag)) {
    selectedTags.value = selectedTags.value.filter((t) => t !== tag);
  } else {
    selectedTags.value.push(tag);
  }
};

const isValid = computed(() => {
  return (
    typeof age.value === "number" &&
    age.value >= 1 &&
    age.value <= 110 &&
    username.value.length >= 1 &&
    username.value.length <= 30 &&
    password.value.length >= 1 &&
    password.value.length <= 30 &&
    password.value === passwordCheck.value &&
    nickname.value.length >= 1 &&
    nickname.value.length <= 30 &&
    selectedTags.value.length >= 1
  );
});

const handleSignup = async () => {
  try {
    const payload = {
      username: username.value,
      password: password.value,
      nickname: nickname.value,
      age: age.value,
      tags: selectedTags.value,
    };

    const res = await axios.post(
      "http://localhost:8000/api/auth/signup",
      payload
    ); // ← 여기 수정됨
    auth.setToken(res.data.token);
    alert("회원가입 성공! 🎉");
    router.push("/login");
  } catch (err) {
    const msg = err.response?.data?.error || "회원가입 중 오류 발생";
    alert(msg);
  }
};
</script>

<style scoped>
.signup-wrapper {
  margin-top: 60px;
  padding: 2rem;
  padding-right: 5px;
  padding-left: 5px;
  background: transparent;
  color: white;
  display: flex;
  justify-content: center;
}
.signup-box {
  background: linear-gradient(
    to bottom,
    rgba(40, 40, 40, 0.9),
    rgba(10, 10, 10, 0.85)
  ); /* 진회색 → 검정 */
  padding: 2rem 5rem 3rem;
  border-radius: 12px;
  width: 450px;
  text-align: center;
  color: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.4); /* 약간의 그림자 */
  backdrop-filter: blur(4px); /* 부드러운 느낌 추가 */
}

.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}
.logo {
  width: 64px;
  margin-bottom: 0.5rem;
  margin-right: 1rem;
}
.brand-text {
  font-family: "GongGothicMedium", sans-serif;
  color: #bc93ff;
  font-size: 2.4rem;
  margin-bottom: 1.5rem;
}
input {
  display: block;
  width: 100%;
  padding: 0.7rem;
  margin-bottom: 1rem;
  border: none;
  border-radius: 6px;
  background-color: #444;
  color: white;
}
.tag-label {
  text-align: left;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #ccc;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: flex-start;
}
.tag-list button {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  background: #ccc;
  color: black;
  border: none;
  cursor: pointer;
  font-weight: bold;
}
.tag-list button.selected {
  background: #b388f0;
  color: white;
}
.submit-btn {
  margin-top: 1rem;
  width: 100%;
  padding: 0.7rem;
  border: none;
  border-radius: 6px;
  background: linear-gradient(to right, #d17df4, #8d5cf6);
  color: white;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
}
</style>
