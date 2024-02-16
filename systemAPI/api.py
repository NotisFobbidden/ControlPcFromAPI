from scheduler import schedule, run_action, pp_queue
import system
from flask import *
import pyautogui as pag

app = Flask(__name__)

# Just a basic flask listener
@app.route('/', methods=['POST'])
def get_request():
    print('[ + ] Got request')
    json_action_info = request.get_json(force=True)
    schedule(json_action_info, int(json_action_info['time']))
    return {"status": "ok"}

@app.route('/', methods=['GET'])
def get_request_get():
    queue_sum = pp_queue()
    return queue_sum