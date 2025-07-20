from django.contrib import admin
from .models import Category, Book

# 管理画面のタイトルとヘッダーをカスタマイズ
admin.site.site_header = "図書管理システム"
admin.site.site_title = "図書管理"
admin.site.index_title = "図書管理システム"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ["name"]
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "isbn", "category", "total_copies", "available_copies", "available"]
    list_filter = ["category", "available", "author", "publisher", "created"]
    search_fields = ["title", "author", "isbn"]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ["available", "available_copies", "total_copies"]
    list_per_page = 20
    
    # フィールドをグループ化して見やすく
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('詳細情報', {
            'fields': ('isbn', 'description', 'publication_date', 'publisher')
        }),
        ('在庫管理', {
            'fields': ('total_copies', 'available_copies', 'available')
        }),
        ('画像', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )
    
    # 本を追加する際のデフォルト値を設定
    def get_changeform_initial_data(self, request):
        return {
            'available': True,
            'total_copies': 1,
            'available_copies': 1,
        }
    
    # 保存時にavailable_copiesがtotal_copiesを超えないようにチェック
    def save_model(self, request, obj, form, change):
        if obj.available_copies > obj.total_copies:
            obj.available_copies = obj.total_copies
        # available_copiesが0の場合、availableをFalseに設定
        if obj.available_copies == 0:
            obj.available = False
        elif obj.available_copies > 0:
            obj.available = True
        super().save_model(request, obj, form, change)
