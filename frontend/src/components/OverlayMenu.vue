<template>
  <aside :class="['overlay-sidebar', { open: isOpen }]">
    <div class="menu">
      <h3 class="section-title" v-if="isOpen">바로가기</h3>
      <ul class="sidebar-nav">
        <li>
          <RouterLink
            to="/"
            :class="{ active: $route.path === '/' }"
            class="nav-item"
          >
            <House class="icon" />
            <span v-if="isOpen">메인</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/myfavorites"
            :class="{ active: $route.path === '/myfavorites' }"
            class="nav-item"
          >
            <AudioLines class="icon" />
            <span v-if="isOpen">당신의 아리아</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/bestsellers"
            :class="{ active: $route.path === '/bestsellers' }"
            class="nav-item"
          >
            <Flame class="icon" />
            <span v-if="isOpen">베스트 셀러</span>
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/newbook"
            :class="{ active: $route.path === '/newbook' }"
            class="nav-item"
          >
            <Sparkle class="icon" />
            <span v-if="isOpen">신착 도서</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/recommendations"
            :class="{ active: $route.path === '/recommendations' }"
            class="nav-item"
          >
            <Feather class="icon" />
            <span v-if="isOpen">블로거 추천 도서</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/reviews"
            :class="{ active: $route.path === '/reviews' }"
            class="nav-item"
          >
            <BookOpenCheck class="icon" />
            <span v-if="isOpen">도서 리뷰</span>
          </RouterLink>
        </li>
      </ul>

      <h3 class="section-title" v-if="isOpen">장르</h3>
      <ul class="sidebar-nav">
        <li>
          <RouterLink
            to="/genre/all"
            :class="{ active: $route.path === '/genre/all' }"
            class="nav-item"
          >
            <!-- ✅ 장르 아이콘은 열렸을 때만 렌더 -->
            <LibraryBig class="icon" v-if="isOpen" />
            <span v-if="isOpen">전체</span>
          </RouterLink>
        </li>
        <li v-for="genre in genres" :key="genre.id">
          <RouterLink
            :to="`/genre/${genre.id}`"
            :class="{ active: $route.path === `/genre/${genre.id}` }"
            class="nav-item"
          >
            <component
              v-if="isOpen"
              :is="genreIcons[genre.name] || LibraryBig"
              class="icon"
            />
            <span v-if="isOpen">{{ genre.name }}</span>
          </RouterLink>
        </li>
      </ul>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import {
  AlignJustify,
  Ellipsis,
  Download,
  Feather,
  Heart,
  Star,
  AudioLines,
  Headphones,
  MessageSquareHeart,
  Music3,
  Music2,
  Music,
  Piano,
  Pin,
  PinOff,
  Save,
  Sparkle,
  Sparkles,
  Sprout,
  ThumbsUp,
  ThumbsDown,
  Flame,
  Award,
  ChevronLeft,
  ChevronRight,
  House,
  BookOpenCheck,
  LibraryBig,
  BookHeart,
  BookUp,
  BookUser,
  BookImage,
  BookHeadphones,
  BookType,
  BookAudio,
} from "lucide-vue-next";

const genres = ref([]);

const genreIcons = {
  all: LibraryBig,
  "소설/시/희곡": BookHeart,
  "경제/경영": BookUp,
  자기계발: BookUser,
  "인문/교양": BookImage,
  "취미/실용": BookHeadphones,
  "어린이/청소년": BookType,
  과학: BookAudio,
};

defineProps({ isOpen: Boolean });

onMounted(async () => {
  try {
    const res = await axios.get("/api/genres/");
    genres.value = res.data;
  } catch (err) {
    console.error("장르 목록 로딩 실패:", err);
  }
});
</script>

<style scoped>
.overlay-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  background: #111;
  width: 64px;
  transition: width 0.3s ease;
  overflow: hidden; /* 스크롤 제거 */
  z-index: 1000;
}
.overlay-sidebar.open {
  width: 250px;
}
.menu {
  background: #111;
  height: 100%;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
}

.sidebar-nav {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: white;
  font-weight: 500;
  padding: 0.5rem 0.6rem;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease;
}

.nav-item .icon {
  width: 18px;
  height: 18px;
  color: #aaa;
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.nav-item:hover {
  background-color: #222;
  color: #b388f0;
}

.nav-item:hover .icon {
  color: #b388f0;
}

.nav-item.active {
  color: #b388f0;
}

.nav-item.active .icon {
  color: #b388f0;
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
}

.section-title {
  color: #888;
  font-size: 0.85rem;
  margin: 5rem 0 0.5rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 0; /* 항목 간 마진 제거 */
}

a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
  display: flex;
  align-items: center;
}

a.active {
  color: #b388f0;
}

a:hover {
  color: #b388f0;
  background-clip: unset;
  -webkit-background-clip: unset;
  -webkit-text-fill-color: unset;
}

.icon {
  width: 20px;
  height: 20px;
  color: #aaa;
  flex-shrink: 0;
  margin-left: 0.5rem;
}
</style>
