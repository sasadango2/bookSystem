from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MemberProfile(models.Model):
    MEMBERSHIP_TYPES = [
        ('student', '学生'),
        ('admin', '管理者'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES, default='student')
    member_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    max_loans = models.PositiveIntegerField(default=5)  # 最大貸出冊数
    loan_period_days = models.PositiveIntegerField(default=14)  # 貸出期間（日数）
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.member_id})"
    
    @property
    def current_loans_count(self):
        return self.user.loans.filter(status='borrowed').count()
    
    @property
    def can_borrow(self):
        return self.is_active and self.current_loans_count < self.max_loans
    
    @property
    def overdue_loans_count(self):
        overdue_count = 0
        for loan in self.user.loans.filter(status='borrowed'):
            if loan.is_overdue:
                overdue_count += 1
        return overdue_count


class LibraryNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('due_reminder', '返却期限リマインダー'),
        ('overdue', '延滞通知'),
        ('reservation_available', '予約書籍利用可能'),
        ('system', 'システム通知'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"