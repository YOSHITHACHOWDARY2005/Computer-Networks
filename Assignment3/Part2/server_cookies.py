import socket

HOST = "127.0.0.1"
PORT = 9000  # server will run on port 9000

WELCOME_NEW = "<h1>Hello, new user! Setting your cookie...</h1>"
WELCOME_BACK = "<h1>Welcome back! Your cookie: {cookie}</h1>"

def get_headers(request_text: str) -> dict:
    # Extract HTTP headers into a dictionary
    headers = {}
    for line in request_text.split("\r\n")[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.strip()] = v.strip()
    return headers

def make_response(content: str, cookie: str = None) -> str:
    # Build HTTP response with optional Set-Cookie header
    header = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(content)}\r\n"
        "Connection: close\r\n"
    )
    if cookie:
        header += f"Set-Cookie: {cookie}\r\n"
    return header + "\r\n" + content

def handle_client(conn: socket.socket):
    # Handle one client: read request, check cookie, send response
    request = conn.recv(1024).decode("utf-8")
    if not request:
        return
    headers = get_headers(request)
    client_cookie = headers.get("Cookie")

    if client_cookie:
        body = WELCOME_BACK.format(cookie=client_cookie)
        response = make_response(body)
    else:
        response = make_response(WELCOME_NEW, cookie="UserID=User123")

    conn.sendall(response.encode("utf-8"))

def run_server():
    # Main server loop: accept clients and handle them
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server is live at http://{HOST}:{PORT}/")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                handle_client(conn)

if __name__ == "__main__":
    run_server()
