from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('books:book_list_by_category', kwargs={'category_slug': self.slug})
    

class Book(models.Model):
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.CharField(max_length=250)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=250)
    available_copies = models.PositiveIntegerField(default=1)
    total_copies = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='books', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'id':self.id, 'slug':self.slug})
    
    @property
    def is_available(self):
        return self.available and self.available_copies > 0
    
    def save(self, *args, **kwargs):
        # available_copiesがtotal_copiesを超えないようにする
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        
        # available_copiesが0の場合、availableをFalseに
        if self.available_copies == 0:
            self.available = False
        elif self.available_copies > 0 and not self.available:
            self.available = True
            
        super().save(*args, **kwargs)
    
        
    
    