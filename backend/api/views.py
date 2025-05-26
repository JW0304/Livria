from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Author, Category, Genre, EmotionTag, Review, Music, MusicReaction
from .serializers import (
    BookSerializer,
    SimilarBookSerializer,
    AuthorSerializer,
    CategorySerializer,
    GenreSerializer,
    EmotionTagSerializer,
    ReviewSerializer,
    MusicSerializer,
    MusicReactionSerializer
)

# ────────────────────────────────────────────────────────────────────────────────
#                       도서 CRUD + 추천 도서 endpoint
# ────────────────────────────────────────────────────────────────────────────────
class BookViewSet(viewsets.ModelViewSet):
    """
    도서 CRUD (읽기: 모두, 쓰기/수정/삭제: 인증 사용자)
    retrieve 시에는 nested로 추천 도서(similar_books) 정보 포함
    추가로 /api/books/{pk}/similar/ 로 추천 도서 4권만 반환
    """
    queryset = Book.objects.select_related('author', 'category', 'genre')\
                           .prefetch_related('similar_books')\
                           .all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'genre']
    search_fields = ['title', 'author__name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'similar']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['get'], permission_classes=[AllowAny], url_path='similar')
    def similar(self, request, pk=None):
        """
        /api/books/{pk}/similar/ : 추천 도서 4권만 반환
        """
        book = self.get_object()
        sims = book.similar_books.all()[:4]
        serializer = SimilarBookSerializer(sims, many=True, context={'request': request})
        return Response(serializer.data)


# ────────────────────────────────────────────────────────────────────────────────
#                       기타 읽기 전용 ViewSet
# ────────────────────────────────────────────────────────────────────────────────
class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('books').all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class EmotionTagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    감정 태그 읽기
    """
    queryset = EmotionTag.objects.all()
    serializer_class = EmotionTagSerializer
    permission_classes = [AllowAny]


# ────────────────────────────────────────────────────────────────────────────────
#                       리뷰 전용 커스텀 퍼미션 및 ViewSet
# ────────────────────────────────────────────────────────────────────────────────
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    SAFE_METHODS(GET, HEAD, OPTIONS)은 모두 허용,
    POST/PUT/PATCH/DELETE 등 수정 요청은 작성자(user) 본인만 허용.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ReviewViewSet(viewsets.ModelViewSet):
    """
    리뷰 CRUD (읽기: 모두, 쓰기/수정/삭제: 인증 사용자)
    """
    queryset = Review.objects.select_related('book', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ────────────────────────────────────────────────────────────────────────────────
#                       음악 & 리액션 ViewSet
# ────────────────────────────────────────────────────────────────────────────────
class MusicViewSet(viewsets.ModelViewSet):
    """
    자동생성 음악 기록의 CRUD
    """
    queryset = Music.objects.select_related('book').all()
    serializer_class = MusicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_music(request, music_id):
    is_like = request.data.get('is_like')
    if is_like is None:
        return Response({'error': 'is_like 값이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    reaction, created = MusicReaction.objects.update_or_create(
        user=request.user,
        music_id=music_id,
        defaults={'is_like': is_like}
    )
    return Response({'detail': '반응 저장 완료'})
