"""
Django admin configuration for books application.
This file configures the Django admin interface for managing models.
"""
from django.contrib import admin
from .models import Book, Author, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Author model
    """
    list_display = ('full_name', 'email', 'birth_date', 'created_at')
    list_filter = ('created_at', 'birth_date')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'birth_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model
    """
    list_display = ('title', 'author', 'category', 'status', 'price', 'publication_date')
    list_filter = ('status', 'category', 'publication_date', 'created_at')
    search_fields = ('title', 'isbn', 'author__first_name', 'author__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'isbn', 'description', 'author', 'category')
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'pages', 'price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize the queryset by selecting related objects
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'category')