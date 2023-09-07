import logging

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django')  # Используйте нужное имя логгера

    def __call__(self, request):
        # Здесь можно выполнять код перед обработкой запроса
        self.logger.debug(f"Request: {request.method} {request.path}")

        response = self.get_response(request)

        # Здесь можно выполнять код после обработки запроса
        self.logger.debug(f"Response: {response.status_code}")

        return response
