// stores/auth.js
import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    user: null,
    error: "",
  }),

  actions: {
    setToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
      axios.defaults.headers.common["Authorization"] = `Token ${token}`;
      console.log("[setToken] 토큰 설정 완료:", token);
    },

    clearToken() {
      this.token = "";
      localStorage.removeItem("token");
      delete axios.defaults.headers.common["Authorization"];
      console.log("[clearToken] 토큰 제거 완료");
    },

    async login(credentials) {
      try {
        const { data } = await axios.post("/auth/login", credentials);

        this.setToken(data.token);
        this.user = data.user;

        localStorage.setItem("nickname", data.user.nickname);
        localStorage.setItem("avatarUrl", data.user.avatar_url); // 사용자 프로필 이미지 경로

        this.error = "";
        console.log("[login] 로그인 성공:", this.user);
      } catch (err) {
        this.error = "로그인에 실패했습니다.";
        console.error("[login] 로그인 실패:", err);
        throw err;
      }
    },

    async signup(payload) {
      try {
        const { data } = await axios.post("/auth/signup", payload);
        this.setToken(data.token);
        this.user = data.user;
        console.log("[signup] 회원가입 성공:", this.user);
      } catch (err) {
        console.error("[signup] 회원가입 실패:", err);
        throw err;
      }
    },

    async fetchMe() {
      if (!this.token) {
        console.warn("[fetchMe] 토큰 없음, 요청 중단");
        return;
      }

      try {
        const { data } = await axios.get("/auth/users/me");
        this.user = data;
        console.log("[fetchMe] 사용자 정보 불러오기 성공:", data);
      } catch (err) {
        console.error("[fetchMe] 실패:", err);
        this.user = null;
        this.clearToken();
      }
    },

    async logout() {
      this.clearToken();
      this.user = null;
      console.log("[logout] 로그아웃 완료");
    },

    async init() {
      const token = localStorage.getItem("token");
      console.log("[init] 초기 토큰:", token);
      if (token) {
        this.setToken(token);
        console.log("[init] 토큰으로 fetchMe 시도");
        await this.fetchMe();
      } else {
        console.log("[init] 저장된 토큰 없음");
      }
    },
  },
});
