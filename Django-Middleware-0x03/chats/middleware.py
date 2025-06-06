import logging
from datetime import datetime
from django.http import HttpResponseForbidden, HttpResponse
import time
from collections import defaultdict, deque

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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of POST requests per IP
        self.ip_message_times = defaultdict(deque)
        self.limit = 5  # messages
        self.window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            times = self.ip_message_times[ip]
            # Remove timestamps older than 1 minute
            while times and now - times[0] > self.window:
                times.popleft()
            if len(times) >= self.limit:
                return HttpResponse('Too many messages sent. Please wait before sending more.', status=429)
            times.append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
