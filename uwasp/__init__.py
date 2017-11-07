__all__ = [
    'WebSocketMiddleware'
]

try:
    import uwsgi
    from .middleware import WebSocketMiddleware
except ImportError:
    class WebSocketMiddleware(object):
        def __init__(self, application, *args, **kwargs):
            self.application = application

        def __call__(self, environ, start_response):
            if environ.get('HTTP_UPGRADE', '').lower() == 'websocket':
                start_response('400 Bad Request', [])
                return []
            else:
                return self.application(environ, start_response)
