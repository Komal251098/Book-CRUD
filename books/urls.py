"""
URL patterns for the books application.
This file defines the routing for book-specific endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .register_view import RegisterView

# Create a router for the viewsets
router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'categories', views.CategoryViewSet)

# URL patterns
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    path('api-auth/register/', RegisterView.as_view(), name='register'),
]