from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Book(models.Model):
    title                  = models.CharField(max_length=200)
    author                 = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_url              = models.URLField()
    description            = models.TextField(blank=True)
    isbn                   = models.CharField(max_length=20, unique=True)
    pub_date               = models.DateField()
    category               = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    global_recommend_count = models.PositiveIntegerField(default=0)
    def __str__(self): return self.title

class EmotionTag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self): return self.name



class Review(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Review by {self.user.username}"
