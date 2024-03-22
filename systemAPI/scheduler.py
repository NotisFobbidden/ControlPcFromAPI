from sortedcontainers import SortedDict
from threading import Event, Thread
from time import time
import system
import pyautogui as pag


class Queue():
    
    def __init__(self) -> None:
        self.queue = SortedDict({})
        self.recheck_signal = Event()
        

    def executor(self):
        while True:
            try:
                # Wait for the next job or the next signal
                max_timeout = self.queue.peekitem(0)[0] - time()
                self.recheck_signal.wait(timeout=max_timeout)
            except:
                # If there are no jobs, just wait
                self.recheck_signal.wait()
            self.recheck_signal.clear()
            self.run_tasks()
        
    def run_tasks(self):
        now = time()
        while True:
            try: 
                # If it's time to run this shit
                if self.queue.peekitem(0)[0] <= now:
                    # Run this shit
                    action = self.queue.popitem(0)[1]
                    Thread(target=lambda: run_action(action), daemon=True).start()
                else:
                    break
            except:
                # If we ran out of elements
                break
            
    def schedule(self, action, timeout):
        deadline = time() + timeout
        self.queue.update({deadline: action})
        try:
            # If the new task is to be executed earlier than the current earliest one
            if self.queue.peekitem(0) >= deadline:
                # Send a recheck signal
                self.recheck_signal.set()
        except:
            self.recheck_signal.set()

    def get_queue(self):
        return self.queue


    # Return the queue in a pretty way to show it on the page
    def pp_queue(self):
        now = time()
        queue_summary = ''
        for t, f in self.get_queue().items():
            queue_summary += f'{self.format_action(f)}{round(t - now, 2)} seconds<br>'
        return queue_summary

    def run_action(self, request):
        match request['action']:
            case 'shutdown_action':
                system.shutdown()
            case 'restart_action':
                system.restart()
            case 'click_action':
                pag.click()
            case 'type_action':
                pag.write(request['text'], interval=0.15)


    # Just a function for pretty formating of the text for queue and debugging
    def format_action(self, request):
        match request['action']:
            case 'shutdown_action':
                return 'Shutting computer down in '
            case 'restart_action':
                return 'Restarting computer in '
            case 'click_action':
                return 'Making a click in '
            case 'type_action':
                text = request['text']
                return f'Typing {text} in '