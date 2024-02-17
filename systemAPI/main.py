from http.server import *
from threading import Thread
from api import app
import os
from scheduler import executor

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.getcwd(), 'webInterface'), **kwargs)


def run_server():
    host = '127.0.0.1'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Server running at http://{host}:{port}")
    httpd.serve_forever()
 
def main():
    flask_thread = Thread(target=lambda: app.run(port=8080, threaded=True))
    flask_thread.start()
    web_app_thread = Thread(target=run_server)
    web_app_thread.start()
    executor_thread = Thread(target=executor)
    executor_thread.start()
    flask_thread.join()
    web_app_thread.join()
    executor_thread.join()

if __name__ == '__main__':
    main()
