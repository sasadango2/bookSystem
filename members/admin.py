from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import MemberProfile

# デフォルトのUser管理を無効化
admin.site.unregister(User)

# カスタムUser管理
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_active", "date_joined"]
    list_filter = ["is_active", "is_staff", "date_joined"]
    search_fields = ["username", "first_name", "last_name", "email"]
    list_per_page = 20
    
    # 簡単なフィールドセット
    fieldsets = (
        ('基本情報', {
            'fields': ('username', 'password')
        }),
        ('個人情報', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('権限', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "member_id", "membership_type", "is_active", "join_date"]
    list_filter = ["membership_type", "is_active", "join_date"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "member_id"]
    readonly_fields = ["join_date", "member_id"]
    list_per_page = 20
    
    fieldsets = (
        ('会員情報', {
            'fields': ('user', 'member_id', 'membership_type', 'is_active')
        }),
        ('日付情報', {
            'fields': ('join_date',),
            'classes': ('collapse',)
        }),
    )
    