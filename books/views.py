from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Book

def book_list(request, category_slug=None):
    category = None
    books = Book.objects.filter(available=True)
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)
    
    return render(request, 'books/book/list.html', {
        'category':category,
        'books':books,
        'categories':categories,
    })
    
def book_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug, available=True)
    return render(request, 'books/book/detail.html', {'book':book})

def book_search(request):
    query = request.GET.get('q')
    books = []
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(description__icontains=query)
        ).filter(available=True)
    
    return render(request, 'books/book/search.html', {
        'books': books,
        'query': query
    })