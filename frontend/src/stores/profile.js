// src/stores/profile.js
import { defineStore } from "pinia";
import axios from "axios";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    id: null,
    username: "",
    email: "",
    nickname: "",
    age: null,
    statusMessage: "",
    avatarUrl: "",
    defaultAvatar: "",
    emotionTags: [],
    favorites: [],
    readBooks: [],
    error: null,
  }),

  actions: {
    // GET /api/auth/users/me  ← 끝에 슬래시 없음!
    async fetchMe() {
      try {
        const { data } = await axios.get("/api/auth/users/me");
        this.id = data.id;
        this.username = data.username;
        this.email = data.email;
        this.nickname = data.nickname;
        this.age = data.age;
        this.statusMessage = data.status_message;
        this.avatarUrl = data.avatar_url;
        this.defaultAvatar = data.default_avatar;
        this.emotionTags = data.emotion_tags;
        this.favorites = data.favorites;
        this.readBooks = data.read_books;
        this.error = null;
      } catch (err) {
        console.error("[profile] fetchMe 실패:", err);
        this.error = err;
      }
    },

    // PATCH /api/auth/users/me  ← 끝에 슬래시 없음!
    async updateMe(payload) {
      try {
        const { data } = await axios.patch("/api/auth/users/me", payload);
        this.nickname = data.nickname;
        this.age = data.age;
        this.statusMessage = data.status_message;
        this.avatarUrl = data.avatar_url;
        this.defaultAvatar = data.default_avatar;
        this.emotionTags = data.emotion_tags;
        this.error = null;
      } catch (err) {
        console.error("[profile] updateMe 실패:", err);
        this.error = err;
        throw err;
      }
    },
  },
});
