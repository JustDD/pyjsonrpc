# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import logging
from app import app
from app.lsp import PyLSPServer

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
	app.start_tcp_server('127.0.0.1', 3300, False, PyLSPServer)
