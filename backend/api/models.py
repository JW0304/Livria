from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_url = models.URLField(blank=True)
    summary   = models.TextField(blank=True)
    works     = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Django가 자동으로 생성해 주는 `id = AutoField(primary_key=True)` 를 사용합니다.

    isbn                  = models.CharField(max_length=20, unique=True)
    title                 = models.CharField(max_length=200)
    author                = models.ForeignKey(Author,   on_delete=models.CASCADE)
    publisher             = models.CharField(max_length=100)
    cover_url             = models.URLField()
    description           = models.TextField()
    pub_date              = models.DateField(null=True, blank=True)
    category              = models.ForeignKey(Category, on_delete=models.CASCADE)
    global_recommend_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.isbn})"


class EmotionTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    book       = models.ForeignKey(Book,                  on_delete=models.CASCADE)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.book}"
