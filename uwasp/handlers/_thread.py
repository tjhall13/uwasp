import uwsgi, select, Queue
from threading import Thread, Event

def _listen(ws, recv_event):
    while not ws.closed:
        try:
            select.select([ws], [], [], 2)
            recv_event.set()
        except select.error:
            ws.close()

def _consume(server, recv_queue):
    server.on_open()

    while True:
        msg = recv_queue.get()
        if msg:
            server.on_message(msg)
        else:
            break

class ThreadHandler(object):
    def __init__(self, ws, server):
        self.ws = ws
        self.server = server

    def handle(self, environ, protocol_name=None):
        websocket_key = environ['HTTP_SEC_WEBSOCKET_KEY']
        origin = environ['HTTP_ORIGIN']

        uwsgi.websocket_handshake(websocket_key, origin, protocol_name)

        send_event = False
        close_event = False
        control = Event()

        send_queue = Queue.Queue()
        recv_queue = Queue.Queue()

        def _write(msg):
            send_queue.put(msg)
            send_event = True
            control.set()

        def _close():
            close_event = True
            control.set()

        self.ws.connect(_write, _close)

        listener = Thread(target=_listen, args=[self.ws, control])
        consumer = Thread(target=_consume, args=[self.server, recv_queue])

        listener.start()
        consumer.start()

        while True:
            # Wait on a single control event because
            # we cannot wait on multiple
            control.wait()

            # If the event was neither send nor close
            # set the event type to recv_event
            recv_event = not (send_event or close_event)

            if send_event:
                try:
                    while True:
                        uwsgi.websocket_send(send_queue.get_nowait())
                except Queue.Empty:
                    send_event = False
                    control.clear()
                except IOError:
                    self.ws.close()

            if recv_event:
                try:
                    msg = True

                    while msg:
                        msg = uwsgi.websocket_recv_nb()
                        if msg: recv_queue.put(msg)

                    control.clear()
                except IOError:
                    self.ws.close()

            if close_event:
                break

        # Put None into the queue to
        # signal end of message events
        recv_queue.put(None)

        consumer.join()
        self.server.on_close()

        # Cannot kill the thread so wait
        # until it times out and ends the
        # loop
        listener.join()

        return []
