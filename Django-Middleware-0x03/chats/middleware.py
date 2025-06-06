import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Set up a module-level logger
logger = logging.getLogger('request_logger')
if not logger.hasHandlers():
    handler = logging.FileHandler('requests.log')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        username = user.username if user and hasattr(user, 'username') and user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {username} - Path: {request.path}"
        logger.info(log_message)
        # Flush the handler to ensure the log is written immediately
        for handler in logger.handlers:
            handler.flush()
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Restrict access outside 6PM (18:00) to 9PM (21:00)
        if not (now >= datetime.strptime('18:00', '%H:%M').time() and now <= datetime.strptime('21:00', '%H:%M').time()):
            return HttpResponseForbidden('Access to the messaging app is restricted during these hours.')
        return self.get_response(request)
