"""
Tests for the books application.
This file contains unit tests for models, views, and other components.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

from .models import Book, Author, Category


class AuthorModelTest(TestCase):
    """
    Test cases for Author model
    """
    
    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            birth_date=date(1980, 1, 1)
        )
    
    def test_author_creation(self):
        """Test that an author can be created successfully"""
        self.assertEqual(self.author.first_name, 'John')
        self.assertEqual(self.author.last_name, 'Doe')
        self.assertEqual(str(self.author), 'John Doe')
    
    def test_full_name_property(self):
        """Test the full_name property"""
        self.assertEqual(self.author.full_name, 'John Doe')


class BookModelTest(TestCase):
    """
    Test cases for Book model
    """
    
    def setUp(self):
        self.author = Author.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        self.category = Category.objects.create(
            name='Fiction',
            description='Fiction books'
        )
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            description='A test book',
            publication_date=date(2023, 1, 1),
            pages=300,
            price=Decimal('19.99'),
            author=self.author,
            category=self.category
        )
    
    def test_book_creation(self):
        """Test that a book can be created successfully"""
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(str(self.book), 'Test Book')
    
    def test_book_is_available(self):
        """Test the is_available method"""
        self.assertTrue(self.book.is_available())
        
        self.book.status = 'borrowed'
        self.book.save()
        self.assertFalse(self.book.is_available())


class BookAPITest(APITestCase):
    """
    Test cases for Book API endpoints
    """
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author',
            email='test.author@example.com'
        )
        self.category = Category.objects.create(
            name='Test Category'
        )
        self.book_data = {
            'title': 'API Test Book',
            'isbn': '9876543210123',
            'description': 'A book for API testing',
            'publication_date': '2023-01-01',
            'pages': 250,
            'price': '24.99',
            'author': self.author.id,
            'category': self.category.id
        }
        self.book = Book.objects.create(
            title='Existing Book',
            isbn='1111111111111',
            publication_date=date(2022, 1, 1),
            pages=200,
            price=Decimal('15.99'),
            author=self.author,
            category=self.category
        )
    
    def test_get_book_list(self):
        """Test retrieving the list of books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_book_detail(self):
        """Test retrieving a single book"""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Existing Book')
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)"""
        url = reverse('book-list')
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API Test Book')
    
    def test_update_book(self):
        """Test updating a book"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', args=[self.book.id])
        update_data = {'title': 'Updated Book Title'}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
    
    def test_delete_book(self):
        """Test deleting a book"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_book_available_action(self):
        """Test the custom available action"""
        url = reverse('book-available')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)