"""
Models for the books application.
This file defines the database structure and business logic.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Author(models.Model):
    """
    Author model - represents book authors
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    """
    Category model - represents book categories
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model - represents books in the system
    This is our main model for CRUD operations
    """
    
    # Book status choices
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    publication_date = models.DateField()
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Relationships
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def is_available(self):
        """Check if the book is available for borrowing"""
        return self.status == 'available'
    
    def get_age_in_years(self):
        """Calculate how many years since publication"""
        return (timezone.now().date() - self.publication_date).days // 365