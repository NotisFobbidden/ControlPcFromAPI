from scheduler import schedule
import system
from flask import *
import pyautogui as pag

app = Flask(__name__)

# Just a basic flask listener
@app.route('/', methods=['POST'])
def get_request():
    print('[ + ] Got request')
    json_action_info = request.get_json(force=True)
    process_request(json_action_info)
    return True

def process_request(request):
    timeout = int(request['time'])
    match request['action']:
        case 'shutdown_action':
            schedule(system.shutdown(), timeout)
        case 'restart_action':
            schedule(system.restart(), timeout)
        case 'click_action':
            schedule(pag.click(), timeout)
        case 'type_action':
            schedule(pag.write(request['text'], interval=0.15), timeout)