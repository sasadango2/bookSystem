from django.contrib import admin
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug':('name',)}
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "isbn", "available_copies", "total_copies", "available", "created", "category"]
    list_filter = ["category", "available", "author", "publisher"]
    search_fields = ["title", "author", "isbn"]
    prepopulated_fields = {'slug':('title',)}
    list_editable = ["available", "available_copies"]
