"""
Views (Controllers) for the books application.
This file contains the business logic and handles HTTP requests/responses.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone

from .models import Book, Author, Category
from .serializers import (
    BookSerializer, 
    BookCreateSerializer, 
    BookUpdateSerializer,
    AuthorSerializer, 
    CategorySerializer
)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model - handles all CRUD operations
    
    This viewset automatically provides:
    - list: GET /api/v1/books/
    - create: POST /api/v1/books/
    - retrieve: GET /api/v1/books/{id}/
    - update: PUT /api/v1/books/{id}/
    - partial_update: PATCH /api/v1/books/{id}/
    - destroy: DELETE /api/v1/books/{id}/
    """
    queryset = Book.objects.select_related('author', 'category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'author']
    search_fields = ['title', 'description', 'author__first_name', 'author__last_name']
    ordering_fields = ['created_at', 'publication_date', 'title', 'price']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action
        """
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookUpdateSerializer
        return BookSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with additional validation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Additional business logic can be added here
        book = serializer.save()
        
        # Return the created book with full details
        response_serializer = BookSerializer(book)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method with additional validation
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Additional business logic can be added here
        book = serializer.save()
        
        # Return the updated book with full details
        response_serializer = BookSerializer(book)
        return Response(response_serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom delete method with additional checks
        """
        instance = self.get_object()
        
        # Add business logic - e.g., check if book is currently borrowed
        if instance.status == 'borrowed':
            return Response(
                {'error': 'Cannot delete a book that is currently borrowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom action to get only available books
        GET /api/v1/books/available/
        """
        available_books = self.queryset.filter(status='available')
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """
        Custom action to get books by author
        GET /api/v1/books/by_author/?author_id=1
        """
        author_id = request.query_params.get('author_id')
        if not author_id:
            return Response(
                {'error': 'author_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = self.queryset.filter(author_id=author_id)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_as_borrowed(self, request, pk=None):
        """
        Custom action to mark a book as borrowed
        PATCH /api/v1/books/{id}/mark_as_borrowed/
        """
        book = self.get_object()
        
        if book.status != 'available':
            return Response(
                {'error': 'Book is not available for borrowing'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.status = 'borrowed'
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_as_returned(self, request, pk=None):
        """
        Custom action to mark a book as returned
        PATCH /api/v1/books/{id}/mark_as_returned/
        """
        book = self.get_object()
        
        if book.status != 'borrowed':
            return Response(
                {'error': 'Book is not currently borrowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.status = 'available'
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'first_name', 'created_at']
    ordering = ['last_name', 'first_name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']