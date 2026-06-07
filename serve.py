#!/usr/bin/env python3
import os, http.server, socketserver

os.chdir('/Users/tiagoleao/Desktop/WEBSITE')
Handler = http.server.SimpleHTTPRequestHandler
Handler.log_message = lambda *a: None
with socketserver.TCPServer(("", 8000), Handler) as httpd:
    httpd.serve_forever()
