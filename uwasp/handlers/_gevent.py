import uwsgi, gevent
from gevent.event import Event
from gevent.queue import Queue, Empty
from gevent.select import select

def _listen(ws, recv_event):
    while not ws.closed:
        try:
            select([ws], [], [], 5)
            recv_event.set()
        except gevent.select.error:
            ws.close()
        except gevent.GreenletExit:
            pass

def _consume(server, recv_queue):
    server.on_open()

    while True:
        msg = recv_queue.get()
        if msg:
            server.on_message(msg)
        else:
            break

class GeventHandler(object):
    def __init__(self, ws, server):
        self.ws = ws
        self.server = server

    def handle(self, environ, protocol_name=None):
        websocket_key = environ['HTTP_SEC_WEBSOCKET_KEY']
        origin = environ['HTTP_ORIGIN']

        uwsgi.websocket_handshake(websocket_key, origin, protocol_name)

        send_event = Event()
        recv_event = Event()
        close_event = Event()

        send_queue = Queue()
        recv_queue = Queue()

        def _write(msg):
            send_queue.put(msg)
            send_event.set()

        def _close():
            close_event.set()

        self.ws.connect(_write, _close)

        listener = gevent.spawn(_listen, self.ws, recv_event)
        consumer = gevent.spawn(_consume, self.server, recv_queue)

        while True:
            gevent.wait([send_event, recv_event, close_event], None, 1)

            if send_event.is_set():
                try:
                    while True:
                        uwsgi.websocket_send(send_queue.get_nowait())
                except Empty:
                    send_event.clear()
                except IOError:
                    self.ws.close()

            if recv_event.is_set():
                try:
                    msg = True

                    while msg:
                        msg = uwsgi.websocket_recv_nb()
                        if msg: recv_queue.put(msg)

                    recv_event.clear()
                except IOError:
                    self.ws.close()

            if close_event.is_set():
                break

        # Put None into the queue to
        # signal end of message events
        recv_queue.put(None)

        consumer.join()
        self.server.on_close()

        listener.kill()

        return []
