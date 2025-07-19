from django.urls import path
from . import views


app_name = "loans"
urlpatterns = [
    path('', views.loan_list, name="loan_list"),
    path('borrow/<int:book_id>/', views.borrow_book, name="borrow_book"),
    path('return/<int:loan_id>/', views.return_book, name="return_book"),
    path('reserve/<int:book_id>/', views.reserve_book, name="reserve_book"),
    path('reservations/', views.reservation_list, name="reservation_list"),
    path('history/', views.loan_history, name="loan_history"),
]
