import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def __call__(self, request):
        user = getattr(request, 'user', None)
        username = user.username if user and hasattr(user, 'username') and user.is_authenticated else 'Anonymous'
        path = getattr(request, 'path', 'Unknown')
        timestamp = datetime.now().isoformat()
        log_message = f"Timestamp: {timestamp}, User: {username}, Path: {path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response