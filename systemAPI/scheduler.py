from sortedcontainers import SortedDict
from threading import Event, Thread
from time import time

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
                func = queue.popitem(0)[1]
                Thread(target=func, daemon=True).start()
            else:
                break
        except:
            # If we ran out of elements
            break
        
def schedule(task, timeout):
    deadline = time() + timeout
    queue.update({deadline: task})
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
    for t, f in get_queue().items():
        print(f"{f} runs in {t - now} secs")
