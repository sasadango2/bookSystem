from django.urls import path
from . import views


app_name= 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<slug:category_slug>/', views.book_list, name='book_list_by_category'),
    path('book/<int:id>/<slug:slug>/', views.book_detail, name="book_detail"),
    path('search/', views.book_search, name='book_search'),
]