def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', '')
    protocol = environ.get('SERVER_PROTOCOL', '')

    if path == "/info" and method == "GET":
        response_body = f"Method: {method}\nURL: {path}\nProtocol: {protocol}"
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [response_body.encode()]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]
