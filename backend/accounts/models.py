from django.contrib.auth.models import AbstractUser
from django.db import models

# 기본 프로필 이미지 선택지
DEFAULT_AVATAR_CHOICES = [
    ('default1', '기본 프로필 1'),
    ('default2', '기본 프로필 2'),
    ('default3', '기본 프로필 3'),
]

class EmotionTag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    nickname       = models.CharField(max_length=50, blank=True)
    age            = models.PositiveIntegerField(null=True, blank=True)
    # 업로드된 프로필 이미지 파일
    avatar         = models.ImageField(
        upload_to='avatars/', blank=True, null=True
    )
    default_avatar = models.CharField(
        max_length=50,
        choices=DEFAULT_AVATAR_CHOICES,
        blank=True,
        help_text='기본 프로필 이미지 선택'
    )
    status_message = models.TextField(blank=True)
    emotion_tags   = models.ManyToManyField(EmotionTag, blank=True)
    favorites      = models.ManyToManyField(
        'api.Book', blank=True, related_name='favored_by'
    )
    read_books     = models.ManyToManyField(
        'api.Book', blank=True, related_name='read_by'
    )

    def get_avatar_url(self):
        """
        1) 업로드된 avatar 파일이 있으면 그 URL 반환
        2) 없으면 default_avatar 선택지에 대응하는 정적 파일 경로 반환
        """
        if self.avatar:
            return self.avatar.url
        choice_map = {
            'default1': '/static/avatars/default1.png',
            'default2': '/static/avatars/default2.png',
            'default3': '/static/avatars/default3.png',
        }
        return choice_map.get(self.default_avatar, choice_map['default1'])