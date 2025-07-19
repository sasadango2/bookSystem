from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.utils import timezone
from datetime import timedelta


class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('borrowed', '貸出中'),
        ('returned', '返却済み'),
        ('overdue', '延滞中'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='borrowed')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-loan_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            # デフォルトで2週間後を返却期限に設定
            self.due_date = (timezone.now() + timedelta(days=14)).date()
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        if self.status == 'returned':
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (timezone.now().date() - self.due_date).days


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['reservation_date']
        unique_together = ['user', 'book']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} (予約)"
    
