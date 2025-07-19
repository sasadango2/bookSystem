from django.contrib import admin
from .models import MemberProfile, LibraryNotification

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "member_id", "membership_type", "is_active", "join_date", "current_loans_count", "overdue_loans_count"]
    list_filter = ["membership_type", "is_active", "join_date"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "member_id"]
    readonly_fields = ["join_date", "current_loans_count", "overdue_loans_count"]
    
    def current_loans_count(self, obj):
        return obj.current_loans_count
    current_loans_count.short_description = "現在の貸出冊数"
    
    def overdue_loans_count(self, obj):
        return obj.overdue_loans_count
    overdue_loans_count.short_description = "延滞冊数"

@admin.register(LibraryNotification)
class LibraryNotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "notification_type", "title", "created_at", "is_read"]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["user__username", "title", "message"]
    date_hierarchy = "created_at"
    