# -*- coding: utf-8 -*-
import os
import socketserver
import logging

log = logging.getLogger(__name__)

class _StreamHandlerWrapper(socketserver.StreamRequestHandler):
    """A wrapper class that is used to construct a custom handler class."""

    delegate = None

    def setup(self):
        super(_StreamHandlerWrapper, self).setup()
        self.delegate = self.DELEGATE_CLASS(self.rfile, self.wfile)

    def handle(self):
        try:
            self.delegate.start()
        except OSError as e:
            if os.name == 'nt':
                # Catch and pass on ConnectionResetError when parent process dies
                if isinstance(e, WindowsError) and e.winerror == 10054:
                    log.error("Cannot start delegate server on Win.")

        self.SHUTDOWN_CALL()
