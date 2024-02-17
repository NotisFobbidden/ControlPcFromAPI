"use strict";
// Send request to the Python API
async function send_request(time, action, text) {
    await fetch('http://localhost:8080/', {
        "method": "POST",
        "body": JSON.stringify({
            'time': time,
            'action': action,
            'text': text
        })
    });
}

// Gets the current queue of tasks and formats it to later be shown on the page
async function get_queue() {
    return await fetch('http://localhost:8080/', {
        "method": "GET"
    }).then((response) => response.text());
}

async function send_request_with_time(action_name, input_id, text) {
    const time = document.getElementById(input_id);
    console.log(time);
    send_request(time.value, action_name, ...(!!text ? [text] : [])); // Only pass text arg if it's not nullish / undefined     
}

// Just some lambdas for each action
const shutdown = () => send_request_with_time("shutdown_action", "shutdown_in");
const restart = () => send_request_with_time("restart_action", "restart_in");
const make_click = () => send_request_with_time('click_action', "click_in");
const type_string = () => send_request_with_time("type_action", "type_in", document.getElementById("type_text").value);

// Made to update the time of tasks in queue "in real time"
setInterval(async () => {
    const queue_container = document.getElementById("queue");
    queue_container.innerHTML = await get_queue();
}, 100);