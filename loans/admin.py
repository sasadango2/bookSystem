from django.contrib import admin
from .models import Loan, Reservation

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "loan_date", "due_date", "return_date", "status", "is_overdue"]
    list_filter = ["status", "loan_date", "due_date"]
    search_fields = ["user__username", "book__title", "book__isbn"]
    date_hierarchy = "loan_date"
    readonly_fields = ["loan_date", "is_overdue", "days_overdue"]
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = "延滞中"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "reservation_date", "is_active", "notified"]
    list_filter = ["is_active", "notified", "reservation_date"]
    search_fields = ["user__username", "book__title"]
    date_hierarchy = "reservation_date"
