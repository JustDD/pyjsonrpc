# -*- coding: utf-8 -*-
import logging
import threading
import socketserver
from functools import partial
from .lsp import PyLSPServer
from .wrapper import _StreamHandlerWrapper


log = logging.getLogger(__name__)


def start_tcp_server(bind_addr, port, check_parent_process, handler_class):
    if not issubclass(handler_class, PyLSPServer):
        raise ValueError('Handler class must be an instance of PythonLSPServer')

    def shutdown_server(check_parent_process, *args):
        if check_parent_process:
            log.debug('Shutting down server')
            # Shutdown call must be done on a thread, to prevent deadlocks
            stop_thread = threading.Thread(target=server.shutdown)
            stop_thread.start()

    # Construct a custom wrapper class around the user's handler_class
    wrapper_class = type(
        handler_class.__name__ + 'Handler',
        (_StreamHandlerWrapper,),
        {'DELEGATE_CLASS': partial(handler_class,
                                   check_parent_process=check_parent_process),
         'SHUTDOWN_CALL': partial(shutdown_server, check_parent_process)}
    )  # 创建一个新的类

    server = socketserver.TCPServer((bind_addr, port), wrapper_class, bind_and_activate=False)
    server.allow_reuse_address = True

    try:
        server.server_bind()
        server.server_activate()
        log.info('Serving %s on (%s, %s)', handler_class.__name__, bind_addr, port)
        server.serve_forever()
    finally:
        log.info('Shutting down')
        server.server_close()


def start_io_server(rfile, wfile, check_parent_process, handler_class):
    if not issubclass(handler_class, PyLSPServer):
        raise ValueError('Handler class must be an instance of PyLSPServer')
    log.info('Starting %s IO language server', handler_class.__name__)
    server = handler_class(rfile, wfile, check_parent_process)
    server.start()
