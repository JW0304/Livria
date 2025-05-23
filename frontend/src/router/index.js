import {
  createRouter,
  createWebHistory,
} from "vue-router";

// 페이지 컴포넌트 임포트
import MainPage from "@/views/MainPage.vue";
import SignupPage from "@/views/SignupPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import PasswordChangePage from "@/views/PasswordChangePage.vue";
import MyPage from "@/views/MyPage.vue";
import BestSellersPage from "@/views/BestSellersPage.vue";
import RecommendationsPage from "@/views/RecommendationsPage.vue";
import BookListPage from "@/views/BookListPage.vue";
import CategoryPage from "@/views/CategoryPage.vue";
import SearchPage from "@/views/SearchPage.vue";
import BookDetailPage from "@/views/BookDetailPage.vue";
import ReviewListPage from "@/views/ReviewListPage.vue";
import FavoritesPage from "@/views/FavoritesPage.vue";
import ReadHistoryPage from "@/views/ReadHistoryPage.vue";
import NotFound from "@/views/NotFound.vue";

// Pinia 스토어 (로그인 확인용)
import { useAuthStore } from "@/stores/auth";

const routes = [
  { path: "/", name: "Main", component: MainPage },
  { path: "/signup", name: "Signup", component: SignupPage },
  { path: "/login", name: "Login", component: LoginPage },
  {
    path: "/password-change",
    name: "PasswordChange",
    component: PasswordChangePage,
    meta: { requiresAuth: true },
  },
  {
    path: "/mypage",
    name: "MyPage",
    component: MyPage,
    meta: { requiresAuth: true },
  },
  { path: "/best-sellers", name: "BestSellers", component: BestSellersPage },
  {
    path: "/recommendations",
    name: "Recommendations",
    component: RecommendationsPage,
  },
  { path: "/books", name: "BookList", component: BookListPage },
  {
    path: "/category/:name",
    name: "Category",
    component: CategoryPage,
    props: true,
  },
  { path: "/search", name: "Search", component: SearchPage },
  {
    path: "/books/:id",
    name: "BookDetail",
    component: BookDetailPage,
    props: true,
  },
  { path: "/reviews", name: "Reviews", component: ReviewListPage },
  {
    path: "/favorites",
    name: "Favorites",
    component: FavoritesPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/read-history",
    name: "ReadHistory",
    component: ReadHistoryPage,
    meta: { requiresAuth: true },
  },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 전역 네비게이션 가드 (로그인 필요 페이지 접근 제어)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.token) {
    next("/login");
  } else {
    next();
  }
});

export default router;