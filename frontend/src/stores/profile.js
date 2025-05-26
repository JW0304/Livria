import { defineStore } from "pinia";
import axios from "axios";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    nickname: "",
    age: null,
    avatarUrl: "", // API 의 avatar_url
    defaultAvatar: "", // API 의 default_avatar
    statusMessage: "",
    emotionTags: [], // ['슬픔과 외로움', ...]
    favorites: [], // Book 객체 리스트
    readBooks: [], // Book 객체 리스트
  }),
  actions: {
    async fetchMe() {
      const { data } = await axios.get("/api/auth/users/me", {
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
      this.$patch({
        nickname: data.nickname,
        age: data.age,
        avatarUrl: data.avatar_url,
        defaultAvatar: data.default_avatar,
        statusMessage: data.status_message,
        emotionTags: Array.isArray(data.emotion_tags)
          ? data.emotion_tags.map((tag) =>
              typeof tag === "string" ? tag : tag.name
            )
          : [],
        favorites: data.favorites ?? [],
        readBooks: data.read_books ?? [],
      });
    },
    async updateMe(payload) {
      // payload: { avatar (File), default_avatar, status_message, emotion_tags, ... }
      const form = new FormData();
      Object.entries(payload).forEach(([k, v]) => form.append(k, v));
      await axios.patch("/api/users/me", form, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
      // 변경 반영
      await this.fetchMe();
    },
  },
});
