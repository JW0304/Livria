import { createRouter, createWebHistory } from "vue-router";

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
import NewBookPage from "@/views/NewBookPage.vue";
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
  { path: "/bestsellers", name: "BestSellers", component: BestSellersPage },
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
    path: "/newbook",
    name: "Newbook",
    component: NewBookPage,
  },
  {
    path: "/readhistory",
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
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();

  // 토큰은 있는데 유저 정보는 없으면 → 사용자 정보 불러오기
  if (auth.token && !auth.user) {
    try {
      await auth.fetchMe();
    } catch (err) {
      // fetchMe 실패 시 토큰 무효화
      auth.logout();
    }
  }

  // 로그인 필요한 페이지인데 로그인 안 되어 있으면 → 로그인 페이지로
  if (to.meta.requiresAuth && !auth.user) {
    next({ name: "Login" });
  } else {
    next();
  }
});

export default router;
