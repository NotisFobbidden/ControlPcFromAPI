from scheduler import Queue
from flask import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
queue = Queue()

# Just a basic flask listener
@app.route('/', methods=['POST'])
def get_request():
    print('[ + ] Got request')
    json_action_info = request.get_json(force=True)
    queue.schedule(json_action_info, int(json_action_info['time']))
    return {"status": "ok"}

@app.route('/', methods=['GET'])
def get_request_get():
    queue_sum = queue.pp_queue()
    return queue_sum