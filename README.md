# 생성형 AI를 활용한 도서 추천 사이트 Livria

> 책(Livre) + 노래(Aria)를 결합한 감성 기반 도서 추천 플랫폼

Livria는 생성형 AI를 활용하여 도서별 맞춤 음악을 생성하고, 코사인 유사도 기반 도서 추천을 제공하는 웹 애플리케이션입니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [시스템 아키텍처](#시스템-아키텍처)
- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [도서 추천 알고리즘](#도서-추천-알고리즘)
- [데이터베이스 모델링](#데이터베이스-모델링)
- [시작하기](#시작하기)
- [API 연동](#api-연동)

## 🎯 프로젝트 개요

Livria는 사용자의 감성과 취향을 반영한 도서 추천과 함께 도서별 맞춤 음악을 제공하는 플랫폼입니다.

### 핵심 기능
- 생성형 AI 기반 도서별 음악 생성
- 코사인 유사도 기반 도서 추천
- GPT 기반 작가 정보 생성
- 사용자 맞춤형 도서 큐레이션

### 프로젝트 정보
- **기간**: 2025.05.20 ~ 05.27 (1주)
- **인원**: 2명

## 🛠 기술 스택

### Frontend
- **Vue.js 3.5.13** - 프론트엔드 프레임워크
- **Vite 6.2.4** - 빌드 도구
- **Vue Router 4.5.0** - 라우팅
- **Pinia 3.0.1** - 상태 관리
- **Axios 1.9.0** - HTTP 클라이언트
- **Swiper 11.2.8** - 캐러셀 컴포넌트
- **Vibrant** - 이미지 색상 추출
- **Sass** - CSS 전처리기

### Backend
- **Python 3.9.13**
- **Django 4.2.21** - 웹 프레임워크
- **Django REST Framework 3.16.0** - API 개발
- **SQLite 3.36** - 데이터베이스
- **scikit-learn 1.6.1** - 머신러닝 (코사인 유사도)
- **NumPy 2.2.6** - 수치 연산
- **BeautifulSoup4 4.13.4** - 웹 스크래핑

### AI & 외부 API
- **OpenAI GPT API** - 작가 정보 생성
- **Wikipedia API** - 작가 정보 탐색
- **Aladin API** - 도서 데이터 수집
- **MusicGen** - 도서 분위기 기반 음악 생성
- **Upstage API** - 선호 도서 기반 도서 추천

### 개발 도구
- **Git / GitHub** - 버전 관리
- **Postman** - API 테스트
- **Figma** - UI/UX 디자인
- **Notion** - 프로젝트 문서화
- **Excalidraw** - 다이어그램 작성

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vue.js)                         │
│              Vue 3 + Pinia + Vue Router                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP / REST API
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend (Django REST Framework)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Accounts    │  │ API         │  │ Services     │       │
│  │ (인증)      │  │ (도서/리뷰)  │  │ (AI 연동)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
         │                │                  │
         │                │                  │
         ↓                ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   SQLite     │  │   OpenAI     │  │   External   │
│   (DB)       │  │   GPT API    │  │   APIs       │
└──────────────┘  └──────────────┘  └──────────────┘
```

## ✨ 주요 기능

### 1. 사용자 관리
- 로그인/회원가입
- 사용자 인증 (JWT)
- 개인정보 수정 (닉네임, 감성 키워드, 비밀번호)
- 프로필 이미지 관리

### 2. 도서 관리
- 도서 CRUD
- 도서 검색 (제목/작가)
- 카테고리별 도서 목록
- 장르 필터링
- 베스트셀러 조회

### 3. 추천 시스템
- **코사인 유사도 기반 유사 도서 추천**
  - 도서 제목과 설명을 벡터화
  - 임베딩 기반 유사도 계산
  - 상위 4개 유사 도서 자동 추천
- **GPT 기반 선호 도서 맞춤형 추천**
  - 사용자 선호 도서 기반 추천
  - 음악과 함께 제공

### 4. 음악 생성 및 추천
- 도서별 맞춤 음악 생성 (MusicGen)
- 음악 미리듣기
- 분위기 태그 표시
- 음악 반응 (좋아요)

### 5. 리뷰 시스템
- 리뷰 CRUD
- 리뷰 좋아요/댓글
- 리뷰 목록 조회

### 6. 개인화 기능
- 읽은 도서 리스트
- 찜한 책 관리
- 나중에 볼 책 저장
- 마이페이지 (프로필, 감성 키워드)

### 7. 작가 정보
- Wikipedia API를 통한 작가 정보 탐색
- GPT API를 통한 작가 정보 생성
- 작가 이미지 및 상세 정보 표시

## 📁 프로젝트 구조

```
Livria/
├── frontend/                  # 프론트엔드
│   ├── src/
│   │   ├── components/       # 공통 컴포넌트
│   │   │   ├── BookCard.vue
│   │   │   ├── BookList.vue
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── Pagination.vue
│   │   ├── views/           # 페이지 컴포넌트
│   │   │   ├── MainPage.vue
│   │   │   ├── BookListPage.vue
│   │   │   ├── BookDetailPage.vue
│   │   │   ├── MyPage.vue
│   │   │   └── ReviewListPage.vue
│   │   ├── stores/          # Pinia 상태 관리
│   │   │   ├── auth.js
│   │   │   ├── books.js
│   │   │   ├── user.js
│   │   │   └── reviews.js
│   │   ├── router/          # Vue Router
│   │   │   └── index.js
│   │   └── assets/          # 정적 리소스
│   ├── package.json
│   └── vite.config.js
│
├── backend/                   # 백엔드
│   ├── accounts/             # 인증 앱
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── api/                  # API 앱
│   │   ├── models.py         # 도서, 리뷰, 음악 모델
│   │   ├── views.py          # API 뷰
│   │   ├── serializers.py   # DRF 시리얼라이저
│   │   ├── services/         # 비즈니스 로직
│   │   │   ├── aladin.py     # Aladin API 연동
│   │   │   ├── music_service.py  # 음악 생성
│   │   │   └── author_media_service.py  # 작가 정보
│   │   └── management/       # Django 커맨드
│   │       └── commands/
│   │           ├── generate_book_music.py
│   │           └── update_similar_books.py
│   ├── livria_backend/       # Django 설정
│   │   ├── settings.py
│   │   └── urls.py
│   ├── requirements.txt
│   └── manage.py
│
└── README.md
```

## 🧮 도서 추천 알고리즘

### 1. 임베딩 기반 추천 (코사인 유사도)

```python
# 도서 제목과 설명을 벡터화
book_embedding = vectorize(book.title + book.description)

# 코사인 유사도 계산
similarity = cosine_similarity(book_embedding, all_book_embeddings)

# 상위 4개 유사 도서 추천
recommended_books = get_top_n_similar(similarity, n=4)
```

**특징:**
- 도서 제목과 설명을 벡터화하여 유사도 계산
- scikit-learn의 cosine_similarity 활용
- 실시간 유사 도서 추천

### 2. GPT 기반 선호 도서 맞춤형 추천

- 사용자의 선호 도서 리스트를 분석
- OpenAI GPT API를 활용한 맞춤형 추천
- 음악과 함께 제공되는 감성 기반 추천

## 🗄️ 데이터베이스 모델링

### 주요 모델

- **User**: 사용자 정보, 감성 키워드
- **Book**: 도서 정보, 임베딩 벡터, 유사 도서 관계
- **Category**: 카테고리 (M:N 관계)
- **Review**: 리뷰 정보
- **Music**: 도서별 생성된 음악
- **MusicReaction**: 음악 반응 (좋아요)

### ERD

```
User ──┬── Review
       ├── Book (읽은 도서, 찜한 도서)
       └── MusicReaction

Book ──┬── Category (M:N)
       ├── Review
       ├── Music
       └── Book (유사 도서, M:N)
```

## 🚀 시작하기

### 필수 요구사항

- **Node.js 18 이상** (Frontend)
- **Python 3.9 이상** (Backend)
- **pip** (Python 패키지 관리)

### 설치 및 실행

#### 1. 저장소 클론

```bash
git clone https://github.com/JW0304/LIVRIA.git
cd Livria
```

#### 2. Backend 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

Backend는 `http://localhost:8000`에서 실행됩니다.

#### 3. Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

Frontend는 `http://localhost:5173`에서 실행됩니다.

### 환경 변수 설정

#### Backend (.env)

```bash
# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Django 설정
SECRET_KEY=your_secret_key
DEBUG=True
```

## 🔌 API 연동

### 외부 API

1. **Aladin API**
   - 도서 정보 수집
   - 도서 검색 및 상세 정보

2. **OpenAI GPT API**
   - 작가 정보 생성
   - 도서 추천 생성

3. **Wikipedia API**
   - 작가 정보 탐색
   - 작가 배경 정보 수집

4. **MusicGen**
   - 도서 분위기 기반 음악 생성
   - 태그 기반 음악 추천

5. **Upstage API**
   - 선호 도서 기반 도서 추천

### API 엔드포인트

#### 인증
- `POST /accounts/signup/` - 회원가입
- `POST /accounts/login/` - 로그인
- `POST /accounts/logout/` - 로그아웃

#### 도서
- `GET /api/books/` - 도서 목록
- `GET /api/books/{id}/` - 도서 상세
- `GET /api/books/{id}/similar/` - 유사 도서
- `GET /api/books/search/` - 도서 검색

#### 리뷰
- `GET /api/reviews/` - 리뷰 목록
- `POST /api/reviews/` - 리뷰 작성
- `PUT /api/reviews/{id}/` - 리뷰 수정
- `DELETE /api/reviews/{id}/` - 리뷰 삭제

#### 음악
- `GET /api/books/{id}/music/` - 도서별 음악
- `POST /api/music/{id}/reaction/` - 음악 반응

## 📝 주요 기술적 특징

### Frontend
- **컴포넌트 기반 아키텍처**: Vue 3 Composition API
- **상태 관리**: Pinia를 통한 전역 상태 관리
- **라우팅**: Vue Router를 통한 SPA 구현
- **UI/UX**: Swiper 캐러셀, 카드 뒤집기 효과
- **이미지 처리**: Vibrant를 통한 이미지 색상 추출

### Backend
- **RESTful API**: Django REST Framework
- **머신러닝 통합**: scikit-learn을 통한 유사도 계산
- **비동기 처리**: 외부 API 호출 최적화
- **데이터 관리**: Django ORM을 통한 데이터베이스 관리
- **커맨드**: Django management commands를 통한 배치 작업

### AI 통합
- **음악 생성**: MusicGen을 통한 도서별 음악 생성
- **텍스트 생성**: GPT API를 통한 작가 정보 생성
- **추천 시스템**: 임베딩 기반 유사도 계산

## 🎬 주요 화면

### 메인 페이지
- 화면 스크롤 및 캐러셀
- 베스트셀러 및 추천 도서 표시

### 도서 목록 페이지
- 도서 검색 기능
- 카테고리별 도서 목록
- 음악 재생 상태 모니터

### 도서 상세 페이지
- API 연결을 통한 작가 정보 생성
- 코사인 유사도 기반 도서 추천
- 도서별 음악 재생

### 프로필 페이지
- 개인 프로필 수정
- 찜한 도서/읽은 도서 목록
- 목록 내 도서 삭제

### 리뷰 목록 페이지
- 마우스 호버 시 카드 뒤집기 효과
- 리뷰 상세 정보 표시

## 👥 팀

- **기간**: 2025.05.20 ~ 05.27 (1주)
- **인원**: 2명

### 역할 분담

#### 프론트엔드 (Vue.js)
- Figma 기반 UI/UX 구현
- 반응형 레이아웃
- Axios를 통한 API 연동
- 음악 추천 UI
- 페이지별 Vue 구성

#### 백엔드 (Django)
- 도서/유저/리뷰 모델 및 API
- 도서 추천 알고리즘 구현
- 음악/도서 생성형 AI 연동
- DB 모델링

#### 공동 작업
- 프론트엔드↔백엔드 크로스 기능 지원
- GitHub 브랜치 협업 및 코드 리뷰
- Notion을 활용한 프로젝트 문서화
- API 연결 테스트 및 디버깅
