"""
Custom middleware for the books application.
Middleware processes requests and responses globally across the application.
"""
import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LoggingMiddleware(MiddlewareMixin):
    """
    Custom middleware to log API requests and responses
    """
    
    def process_request(self, request):
        """
        Process the request before it reaches the view
        """
        # Record the start time
        request.start_time = time.time()
        
        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.path}")
        
        # You can add more request processing logic here
        # For example: rate limiting, request validation, etc.
        
        return None  # Continue processing
    
    def process_response(self, request, response):
        """
        Process the response before it's sent back to the client
        """
        # Calculate processing time
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"Request processed in {duration:.3f}s: {request.method} {request.path} - Status: {response.status_code}")
        
        # Add custom headers
        response['X-API-Version'] = '1.0'
        response['X-Processing-Time'] = f"{duration:.3f}s" if hasattr(request, 'start_time') else 'N/A'
        
        return response
    
    def process_exception(self, request, exception):
        """
        Process any unhandled exceptions
        """
        logger.error(f"Exception in request {request.method} {request.path}: {str(exception)}")
        return None  # Let Django handle the exception


class APIVersionMiddleware(MiddlewareMixin):
    """
    Middleware to handle API versioning
    """
    
    def process_request(self, request):
        """
        Add API version information to the request
        """
        # Extract version from URL path or header
        api_version = request.META.get('HTTP_API_VERSION', '1.0')
        request.api_version = api_version
        
        return None


class CacheControlMiddleware(MiddlewareMixin):
    """
    Middleware to add cache control headers
    """
    
    def process_response(self, request, response):
        """
        Add cache control headers to responses
        """
        if request.path.startswith('/api/'):
            # Add cache headers for API responses
            if request.method == 'GET':
                response['Cache-Control'] = 'public, max-age=300'  # 5 minutes
            else:
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        return response