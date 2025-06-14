import logging

logger = logging.getLogger('django.request')


class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f'[REQUEST] {request.method} {request.path} | headers={dict(request.headers)}')
        if request.method in ('POST', 'PUT', 'PATCH'):
            try:
                body = request.body.decode('utf-8')
                logger.info(f'Body: {body}')
            except Exception:
                logger.warning('Could not decode request body')

        response = self.get_response(request)

        logger.info(f'[RESPONSE] {request.method} {request.path} -> {response.status_code}')
        return response
