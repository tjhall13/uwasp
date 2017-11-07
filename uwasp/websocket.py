import uwsgi

class WebSocket(object):
    def __init__(self):
        self._fileno = uwsgi.connection_fd()
        self.closed = False

    def connect(self, write, close):
        self._write = write
        self._close = close

    def fileno(self):
        return self._fileno

    def send(self, msg):
        if self.closed:
            raise Exception('Cannot send on closed WebSocket')
        else:
            self._write(msg)

    def close(self):
        self.closed = True
        self._close()
