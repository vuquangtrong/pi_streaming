#!/usr/bin/env python3

import http.server

def main():
    server_address = ('', 8000)
    hls_handler = http.server.SimpleHTTPRequestHandler
    
    httpd = http.server.ThreadingHTTPServer(server_address, hls_handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()