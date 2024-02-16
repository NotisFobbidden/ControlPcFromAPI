"use strict";
async function send_request(time, action, text) {
    await fetch('http://127.0.0.1:8080/', {
        "method": "POST",
        "body": JSON.stringify({
            'time': time,
            'action': action,
            'text': text
        }),
        mode: 'no-cors'
    });
}

async function send_request_with_time(action_name, input_id, text) {
    const time = document.getElementById(input_id);
    console.log(time);
    send_request(time.value, action_name, ...(!!text ? [text] : [])); // Only pass text arg if it's not nullish / undefined     
}


const shutdown = () => send_request_with_time("shutdown_action", "shutdown_in");
const restart = () => send_request_with_time("restart_action", "restart_in");
const click = () => send_request_with_time("click_action", "click_in");
const type_string = () => send_request_with_time("type_action", "type_in", document.getElementById("type_text").value);