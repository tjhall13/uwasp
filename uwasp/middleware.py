from .websocket import WebSocket
from .handlers import ThreadHandler

class WebSocketMiddleware(object):
    def __init__(self, application, handler_class=ThreadHandler, servers=[]):
        self.application = application
        self.handler_class = handler_class
        self.server_classes = dict(servers)

    def __call__(self, environ, start_response):
        if environ.get('HTTP_UPGRADE', '').lower() == 'websocket':
            # Retrieve websocket server for current path
            server_class = self.server_classes.get(environ['PATH_INFO'])

            if server_class:
                protocol_name = getattr(server_class, 'PROTOCOL_NAME', None)

                # Construct the websocket object and server
                ws = WebSocket()
                server = server_class(ws)

                # Construct the configured handler to handle
                # the async I/O required for a websocket request
                handler = self.handler_class(ws, server)
                return handler.handle(environ, protocol_name)
            else:
                start_response('404 Not Found', [])
                return []
        else:
            return self.application(environ, start_response)
