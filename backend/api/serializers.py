from rest_framework import serializers
from .models import Book, Review, Author, Category, Genre, EmotionTag, Music

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='book-detail'
    )
    class Meta:
        model  = Author
        fields = ['url','id','name','summary','books']


class EmotionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = EmotionTag
        fields = ['url','id','name']

class MusicSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ["id", "tag", "audio_url"]

    def get_audio_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.audio_file.url)

class BookSerializer(serializers.HyperlinkedModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedIdentityField(view_name="book-detail", read_only=True)
    author           = serializers.HyperlinkedRelatedField(read_only=True, view_name='author-detail')
    category         = serializers.HyperlinkedRelatedField(read_only=True, view_name='category-detail')
    genre            = serializers.HyperlinkedRelatedField(read_only=True, view_name='genre-detail')

    author_name      = serializers.CharField(source='author.name', read_only=True)
    author_summary   = serializers.CharField(source='author.summary', read_only=True)
    author_image_url = serializers.CharField(source='author.image_url', read_only=True)
    
    category_name    = serializers.CharField(source='category.name', read_only=True)
    genre_name       = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'url', 'id', 'isbn', 'title', 'publisher', 'cover_url',
            'description', 'pub_date',
            'category', 'category_name',
            'genre', 'genre_name',
            'author', 'author_name', 'author_summary', 'author_image_url',
            'global_recommend_count', 'musics'
        ]

class CategorySerializer(serializers.ModelSerializer):
    # 기존 Hyperlinked = URL만 돌려주던 부분을 BookSerializer로 교체
    books = BookSerializer(many=True, read_only=True, context={'request': None})
    class Meta:
        model  = Category
        fields = ['id', 'name', 'books']

class GenreSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, context={'request': None})
    class Meta:
        model  = Genre
        fields = ['id', 'name', 'books']

class ReviewSerializer(serializers.ModelSerializer):
    # user 는 읽기 전용 필드로만 노출
    user = serializers.StringRelatedField(read_only=True)
    user_avatar = serializers.SerializerMethodField()

    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # 👈 이거 추가

    def get_user_avatar(self, obj):
        request = self.context.get('request')
        url = obj.user.get_avatar_url()
        return request.build_absolute_uri(url) if url else None
    
    class Meta:
        model  = Review
        fields = ['id', 'book', 'user', 'user_avatar', 'content', 'created_at']
        # fields = ('id', 'book', 'user', 'user_avatar', 'content', 'created_at')
        read_only_fields = ['id', 'user', 'created_at', 'user_avatar']
    