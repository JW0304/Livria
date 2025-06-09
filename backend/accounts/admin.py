from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmotionTag

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 기본 UserAdmin 필드셋에 추가 정보 필드 병합
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': (
                'nickname', 'age', 'avatar', 'default_avatar',
                'status_message', 'emotion_tags', 'favorites', 'read_books'
            ),
        }),
    )
    list_display = (
        'username', 'email', 'nickname', 'age', 'is_staff', 'is_active'
    )
    list_filter  = ('is_staff', 'is_active', 'emotion_tags')

@admin.register(EmotionTag)
class EmotionTagAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
