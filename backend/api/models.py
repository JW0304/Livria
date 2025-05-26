from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Author(models.Model):
    name      = models.CharField(max_length=200, unique=True)
    image_url = models.URLField(blank=True)
    summary   = models.TextField(blank=True)
    works     = models.JSONField(default=list, blank=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    isbn                     = models.CharField(max_length=20, unique=True)
    title                    = models.CharField(max_length=255)
    publisher                = models.CharField(max_length=255, blank=True)
    cover_url                = models.URLField(blank=True)
    description              = models.TextField(blank=True)
    pub_date                 = models.DateField(null=True, blank=True)
    global_recommend_count   = models.IntegerField(default=0)
    author                   = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    category                 = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    genre                    = models.ForeignKey(Genre,    on_delete=models.SET_NULL, null=True, related_name='books')
    # ─── 새로 추가 ───────────────────────────────────────────────────────────
    embedding = models.JSONField(null=True, blank=True)
    recommended_books = models.ManyToManyField(
        'self', blank=True,
        help_text="유사도 상위 N권을 미리 저장"
    )

    def __str__(self):
        return self.title

class EmotionTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Review(models.Model):
    book       = models.ForeignKey(Book, on_delete=models.CASCADE)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review by {self.user}"

class Music(models.Model):
    """
    각 도서(Book)에 대해 생성된 음악 조각을 저장합니다.
    """
    book       = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='musics'
    )
    tag        = models.CharField(max_length=50)  # 예: "슬픔과 외로움"
    audio_file = models.FileField(
        upload_to='book_music/',
        help_text='Generated music clip for this book+tag'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book.title} — {self.tag}'
