# uWASP

An asynchronous uwsgi websocket handler library.

## Class Definitions

### `WebSocketMiddleware(application, handler_class=ThreadHandler, servers=[])`
Constructs a new WSGI application that wraps an existing WSGI application

#### Parameters:
- `application`: is a WSGI application callable. This middleware wraps the WSGI application callable and for non-websocket connections will pass control to this application
- `handler_class`: a handler class to return schedule tasks and queue messages for the server object.
- `servers`: an iterable of tuples, `(path, server_class)`, where the path is the path the wsgi application should mount this server to and the `server_class` is the server class to handle messages and events

### `Handler(ws, server)`
Constructs a new handler object to be used by the middleware

#### Parameters
- `ws`: a `WebSocket` instance to comunicate to the client with
- `server`: a `Server` instance that will handle messages and events

### `Handler.handle(environ, protocol_name=None)`
Handle the current websocket connection. Must return an iterable for the WSGI application

#### Parameters
- `environ`: a WSGI environ dictionary
- `protocol_name`: (optional) protocol name for the websocket

### `Server(ws)`

#### Parameters
- `ws`: a `WebSocket` instance to facilitate communication with the client

### `Server.on_open()`
A method to be called when the websocket is open

### `Server.on_message(message)`
A method to be called when the websocket has a new message from the client.

#### Parameters
- `message`: a `str` object containing the raw message

### `Server.on_close()`
A method to be called when the websocket has closed


## Provided Handlers

### `ThreadHandler`
The default WebSocket handler. This creates a listener thread and consumer thread to handle scheduling messages for the server. This is the default handler class but may only be used if uwsgi has threads enabled.

### `GeventHandler`
Can be used if gevent is installed in the current environment. It is to be used with the uwsgi gevent loop. This will spawn multiple greenlets to schedule messages for the server.

## Server Interface
To take advantage of the websocket middleware, a server should be provided with the tuples of path names and server classes to the middleware.
