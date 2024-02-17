from sortedcontainers import SortedDict
from threading import Event, Thread
from time import time, ctime
import system
import pyautogui as pag

queue = SortedDict({})
recheck_signal = Event()

def executor():
    while True:
        try:
            # Wait for the next job or the next signal
            max_timeout = queue.peekitem(0)[0] - time()
            recheck_signal.wait(timeout=max_timeout)
        except:
            # If there are no jobs, just wait
            recheck_signal.wait()
        recheck_signal.clear()
        run_tasks()
    
def run_tasks():
    now = time()
    while True:
        try: 
            # If it's time to run this shit
            if queue.peekitem(0)[0] <= now:
                # Run this shit
                action = queue.popitem(0)[1]
                Thread(target=lambda: run_action(action), daemon=True).start()
            else:
                break
        except:
            # If we ran out of elements
            break
        
def schedule(action, timeout):
    deadline = time() + timeout
    queue.update({deadline: action})
    try:
        # If the new task is to be executed earlier than the current earlist one
        if queue.peekitem(0) >= deadline:
            # Send a recheck signal
            recheck_signal.set()
    except:
        recheck_signal.set()

def get_queue():
    return queue

def pp_queue():
    now = time()
    queue_summary = ''
    for t, f in get_queue().items():
        queue_summary += f'{format_action(f)}{round(t - now, 2)} seconds<br>'
    return queue_summary

def run_action(request):
    match request['action']:
        case 'shutdown_action':
            system.shutdown()
        case 'restart_action':
            system.restart()
        case 'click_action':
            pag.click()
        case 'type_action':
            pag.write(request['text'], interval=0.15)

def format_action(request):
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
