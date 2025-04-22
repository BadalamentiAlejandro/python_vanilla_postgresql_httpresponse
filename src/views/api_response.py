import json


def send_json_response(handler, data: dict, status=200): # data is dict or list.            
    response_body = json.dumps(data).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(response_body)))
    handler.end_headers()
    handler.wfile.write(response_body)


def send_error_response(handler, message, status=400):
    if isinstance(message, str):
        payload = {"error": message}

    else:
        payload = message
    send_json_response(handler, payload, status)