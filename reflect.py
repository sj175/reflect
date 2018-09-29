#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Forked from https://gist.github.com/huyng/814831

from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import sys, json

class RequestHandler(BaseHTTPRequestHandler):
    cors = False
    
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print("Request type:", self.command)
        print("Request path:", request_path)
        print("Request headers:", self.headers)
        print("<----- Request End -----\n")
        
        self.send_response(200)
        if self.cors:
            self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
    def do_POST(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print("Request type:", self.command)
        print("Request path:", request_path)
        
        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0

        try:
            content = json.loads(self.rfile.read(length))
        except ValueError:
            print("Failed to decode JSON")
            print("<----- Request End -----\n")
            self.send_response(500, 'JSON decode error')
            if self.cors:
                self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return
        
        print("Content Length:", length)
        print("Request headers:", request_headers)
        print("Request payload:", content)
        print("<----- Request End -----\n")
        
        self.send_response(200)
        if self.cors:
            self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    do_PUT = do_POST
    do_DELETE = do_GET
        
def main(port, cors):
    if port is None:
        port = 8080
    if cors is None:
        cors = False

    RequestHandler.cors = cors
    print('Listening on localhost: %s' % port)
    print('Cross origin header present: %s' % cors)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET, PUT, POST or DELETE parameters\n"
                    "Run:\n\n"
                    "   reflect [-c] [-p PORT]")
    parser.add_option("-p", "--port", action="store", type="int", help="the port number to run on")
    parser.add_option("-c", "--cors", action="store_true", dest="cors", help="add Access-Control-Allow-Origin header with value *")
    (options, args) = parser.parse_args()

    main(options.port, options.cors)
