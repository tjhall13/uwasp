try:
    from ._gevent import GeventHandler
except ImportError:
    class GeventHandler(object):
        def __init__(self, *args, **kwargs):
            raise Exception('GeventHandler requires gevent to be installed in the current environment')

from ._thread import ThreadHandler