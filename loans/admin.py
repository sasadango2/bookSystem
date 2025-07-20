from django.contrib import admin
from .models import Loan, Reservation

# 貸出と予約の管理は複雑になるため、管理画面では非表示にする
# 必要に応じて個別に登録可能

# @admin.register(Loan)
# class LoanAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Reservation)  
# class ReservationAdmin(admin.ModelAdmin):
#     pass
