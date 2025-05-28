<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="brand">
        <img src="@/assets/purplelogo.png" alt="Livria 로고" class="logo" />
        <h1 class="brand-text">Livria</h1>
      </div>
      <div class="login-box">
        <p class="welcome">리브리아에 어서오세요!</p>
        <form @submit.prevent="handleLogin">
          <input v-model="username" placeholder="아이디" required />
          <input
            v-model="password"
            type="password"
            placeholder="비밀번호"
            required
          />
          <button type="submit" class="login-btn">로그인</button>
        </form>
        <div class="links">
          <a @click.prevent="goSignup">회원가입</a>
          <a @click.prevent="goReset" class="right">비밀번호 변경</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();
const username = ref("");
const password = ref("");

const handleLogin = async () => {
  try {
    await auth.login({ username: username.value, password: password.value });
    router.push("/");
  } catch (err) {
    console.error(err);
    alert("로그인 실패! 아이디와 비밀번호를 확인해 주세요.");
  }
};

const goSignup = () => router.push("/signup");
const goReset = () => router.push("/reset-password");
</script>

<style scoped>
.login-wrapper {
  margin-top: 70px;
  background-color: black;
  min-height: 100vh;
  background: transparent;
  color: white;
  display: flex;
  justify-content: center;
}
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
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
.login-box {
  background: linear-gradient(
    to bottom,
    rgba(40, 40, 40, 0.9),
    rgba(10, 10, 10, 0.85)
  ); /* 진회색 → 검정 */
  padding: 2rem 5rem 3rem;
  border-radius: 12px;
  width: 320px;
  text-align: center;
  color: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.4); /* 약간의 그림자 */
  backdrop-filter: blur(4px); /* 부드러운 느낌 추가 */
}
.welcome {
  margin-bottom: 1.5rem;
  color: #ccc;
}
input {
  display: block;
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  border: none;
  border-radius: 6px;
  background-color: #444;
  color: white;
}
.login-btn {
  width: 100%;
  padding: 0.6rem;
  border: none;
  border-radius: 6px;
  background: linear-gradient(90deg, #d17df4, #8d5cf6);
  color: white;
  font-weight: bold;
  cursor: pointer;
}
.links {
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #aaa;
  display: flex;
  justify-content: space-between;
}
.links a {
  cursor: pointer;
  text-decoration: underline;
}
</style>
