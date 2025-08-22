"""
Serializers for the books application.
Serializers handle the conversion between Django models and JSON format.
"""
from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model
    """
    full_name = serializers.ReadOnlyField()
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_books_count(self, obj):
        """Return the number of books by this author"""
        return obj.books.count()
    
    def validate_email(self, value):
        """Custom validation for email field"""
        if Author.objects.filter(email=value).exists():
            if self.instance and self.instance.email != value:
                raise serializers.ValidationError("An author with this email already exists.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def get_books_count(self, obj):
        """Return the number of books in this category"""
        return obj.book_set.count()


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model - handles full CRUD operations
    """
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    age_in_years = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_age_in_years(self, obj):
        """Return the age of the book in years"""
        return obj.get_age_in_years()
    
    def get_is_available(self, obj):
        """Return whether the book is available"""
        return obj.is_available()
    
    def validate_isbn(self, value):
        """Custom validation for ISBN field"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be either 10 or 13 characters long.")
        
        if Book.objects.filter(isbn=value).exists():
            if self.instance and self.instance.isbn != value:
                raise serializers.ValidationError("A book with this ISBN already exists.")
        
        return value
    
    def validate_pages(self, value):
        """Custom validation for pages field"""
        if value <= 0:
            raise serializers.ValidationError("Number of pages must be positive.")
        return value
    
    def validate_price(self, value):
        """Custom validation for price field"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class BookCreateSerializer(BookSerializer):
    """
    Specialized serializer for book creation with different validation rules
    """
    class Meta(BookSerializer.Meta):
        fields = [
            'title', 'isbn', 'description', 'publication_date', 
            'pages', 'price', 'status', 'author', 'category'
        ]


class BookUpdateSerializer(BookSerializer):
    """
    Specialized serializer for book updates - allows partial updates
    """
    class Meta(BookSerializer.Meta):
        fields = [
            'title', 'isbn', 'description', 'publication_date', 
            'pages', 'price', 'status', 'author', 'category'
        ]
        extra_kwargs = {
            'title': {'required': False},
            'isbn': {'required': False},
            'publication_date': {'required': False},
            'pages': {'required': False},
            'price': {'required': False},
            'author': {'required': False},
        }