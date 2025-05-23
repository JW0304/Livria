from django.contrib.auth.models import AbstractUser
from django.db import models

class EmotionTag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self): return self.name

class User(AbstractUser):
    nickname       = models.CharField(max_length=50, blank=True)
    age            = models.PositiveIntegerField(null=True, blank=True)
    avatar_url     = models.URLField(blank=True)
    status_message = models.TextField(blank=True)
    emotion_tags   = models.ManyToManyField(EmotionTag, blank=True)
