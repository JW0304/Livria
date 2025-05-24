// src/stores/user.js 또는 user.ts
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    email: '',
  }),
  actions: {
    setUserData(data) {
      this.username = data.username;
      this.email = data.email;
    },
  },
});
