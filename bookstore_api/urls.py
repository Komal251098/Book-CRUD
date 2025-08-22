"""
URL Configuration for bookstore_api project.
This file contains the main URL patterns for the entire project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from books.register_view import RegisterView
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet

# Create a router and register our viewset with it
router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/', include(router.urls)),

    # Additional book-specific URLs
    path('api/v1/', include('books.urls')),

    # DRF authentication URLs
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/register/', RegisterView.as_view(), name='register'),
    path('api-auth/token/', obtain_auth_token, name='api_token_auth'),
]