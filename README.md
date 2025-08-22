# Django REST API Project - Bookstore

A comprehensive Django REST API project demonstrating CRUD operations with a bookstore theme.

## Project Structure

```
bookstore_api/
├── manage.py                 # Django management script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
├── bookstore_api/          # Main project directory
│   ├── __init__.py
│   ├── settings.py         # Django settings and configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
└── books/                  # Books application
    ├── __init__.py
    ├── apps.py            # App configuration
    ├── models.py          # Database models
    ├── serializers.py     # DRF serializers
    ├── views.py           # Views (Controllers)
    ├── urls.py            # App-specific URLs
    ├── middleware.py      # Custom middleware
    ├── admin.py           # Django admin configuration
    ├── tests.py           # Unit tests
    └── migrations/        # Database migrations
        └── __init__.py
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### 2. Installation Steps

1. **Clone or create the project directory:**
   ```bash
   mkdir django-bookstore-api
   cd django-bookstore-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env file with your actual values
   ```

5. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Books
- `GET /api/v1/books/` - List all books
- `POST /api/v1/books/` - Create a new book
- `GET /api/v1/books/{id}/` - Retrieve a specific book
- `PUT /api/v1/books/{id}/` - Update a specific book
- `PATCH /api/v1/books/{id}/` - Partially update a specific book
- `DELETE /api/v1/books/{id}/` - Delete a specific book

### Custom Book Actions
- `GET /api/v1/books/available/` - List available books
- `GET /api/v1/books/by_author/?author_id={id}` - Books by author
- `PATCH /api/v1/books/{id}/mark_as_borrowed/` - Mark book as borrowed
- `PATCH /api/v1/books/{id}/mark_as_returned/` - Mark book as returned

### Authors
- `GET /api/v1/authors/` - List all authors
- `POST /api/v1/authors/` - Create a new author
- `GET /api/v1/authors/{id}/` - Retrieve a specific author
- `PUT /api/v1/authors/{id}/` - Update a specific author
- `DELETE /api/v1/authors/{id}/` - Delete a specific author

### Categories
- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create a new category
- `GET /api/v1/categories/{id}/` - Retrieve a specific category
- `PUT /api/v1/categories/{id}/` - Update a specific category
- `DELETE /api/v1/categories/{id}/` - Delete a specific category

## File Explanations

### Core Django Files

**`manage.py`**: Command-line utility for Django administrative tasks like running the server, creating migrations, etc.

**`bookstore_api/settings.py`**: Contains all Django configuration including database settings, installed apps, middleware, REST framework configuration, and CORS settings.

**`bookstore_api/urls.py`**: Main URL configuration that routes requests to appropriate views. Includes both DRF router URLs and custom URL patterns.

**`bookstore_api/wsgi.py`**: WSGI configuration for deployment to production servers.

### Application Files

**`books/models.py`**: Defines the database structure with three models:
- `Author`: Represents book authors with personal information
- `Category`: Represents book categories  
- `Book`: Main model with relationships to Author and Category

**`books/serializers.py`**: Handles conversion between Django models and JSON format:
- Validation logic for API inputs
- Custom fields and methods
- Different serializers for create/update operations

**`books/views.py`**: Contains the business logic (Controllers):
- `BookViewSet`: Handles all CRUD operations for books
- `AuthorViewSet`: Manages author operations
- `CategoryViewSet`: Manages category operations
- Custom actions for specific business requirements

**`books/urls.py`**: Application-specific URL routing that defines how URLs map to views.

**`books/middleware.py`**: Custom middleware for cross-cutting concerns:
- Request/response logging
- API versioning
- Cache control headers

**`books/admin.py`**: Configuration for Django admin interface to manage data through a web interface.

**`books/tests.py`**: Unit tests for models, API endpoints, and business logic.

## Key Features

1. **Complete CRUD Operations**: Create, Read, Update, Delete for all models
2. **Custom Business Logic**: Book borrowing/returning functionality
3. **Data Validation**: Comprehensive input validation and error handling
4. **Filtering & Search**: Advanced filtering, searching, and ordering capabilities
5. **Pagination**: Built-in pagination for large datasets
6. **Authentication**: Session-based authentication with permission controls
7. **Custom Middleware**: Logging, versioning, and caching middleware
8. **Admin Interface**: Django admin for data management
9. **Comprehensive Testing**: Unit tests for models and API endpoints

## Testing

Run the test suite:
```bash
python manage.py test
```

Run with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Development Commands

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Open Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

This project demonstrates professional Django REST API development with proper separation of concerns, comprehensive error handling, and production-ready features.