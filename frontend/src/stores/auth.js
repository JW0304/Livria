import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    user: JSON.parse(localStorage.getItem("user") || "null"),
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
        const { data } = await axios.post("/api/auth/login", credentials);
        const tok = data.token ?? data.key;
        if (!tok) throw new Error("로그인 응답에 토큰이 없습니다");
        this.setToken(tok);

        this.user = data.user;
        localStorage.setItem("user", JSON.stringify(data.user));
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
        const { data } = await axios.post("/api/auth/signup", payload);
        const tok = data.token ?? data.key;
        if (!tok) throw new Error("회원가입 응답에 토큰이 없습니다");
        this.setToken(tok);

        this.user = data.user;
        localStorage.setItem("user", JSON.stringify(data.user));
        console.log("[signup] 회원가입 성공:", this.user);
      } catch (err) {
        console.error("[signup] 회원가입 실패:", err);
        throw err;
      }
    },

    logout() {
      this.clearToken();
      this.user = null;
      localStorage.removeItem("user");
      console.log("[logout] 로그아웃 완료");
    },

    init() {
      // 1) 토큰 복구
      const token = localStorage.getItem("token");
      console.log("[init] 초기 토큰:", token);
      if (token) {
        this.setToken(token);
      }

      // 2) user 복구
      const u = localStorage.getItem("user");
      if (u) {
        this.user = JSON.parse(u);
        console.log("[init] 로컬스토리지 유저 복원:", this.user);
      } else {
        console.log("[init] 저장된 유저 정보 없음");
      }
    },
  },
});
