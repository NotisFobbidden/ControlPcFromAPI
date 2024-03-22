from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.getcwd(), 'webInterface'), **kwargs)

class Server:
    def __init__(self, host, port, handler=CustomRequestHandler):
        self.host = host
        self.port = port
        self.handler = handler

    def run_server(self):
        server_address = (self.host, self.port)
        httpd = HTTPServer(server_address, self.handler)
        print(f"Server running at http://{self.host}:{self.port}")
        httpd.serve_forever()