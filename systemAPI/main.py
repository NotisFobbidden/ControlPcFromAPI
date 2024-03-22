from http.server import *
from threading import Thread
from api import app
from scheduler import Queue
from server import Server
from rich.console import Console


def main():
    console = Console()
    server = Server(host='127.0.0.1', port=8000)
    queue = Queue()
    flask_thread = Thread(target=lambda: app.run(port=8080, threaded=True))
    flask_thread.start()
    console.print('[cyan1 bold][ + ] Flask thread started![/cyan1 bold]')
    web_app_thread = Thread(target=server.run_server)
    web_app_thread.start()
    console.print('[cyan1 bold][ + ] Web app started![/cyan1 bold]')
    executor_thread = Thread(target=queue.executor)
    executor_thread.start()
    console.print('[cyan1 bold][ + ] Executor thread started![/cyan1 bold]')
    flask_thread.join()
    web_app_thread.join()
    executor_thread.join()

if __name__ == '__main__':
    main()