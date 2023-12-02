# import pytube as yt
# import validators
import socket 
import os
import threading

#Setup--------------------------------------------------------------
HOST = "0.0.0.0"
SERVER_PORT = 8080
FORMAT = "utf8"

def createServerSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, SERVER_PORT))
    s.listen()
    return s

#RenderHTML--------------------------------------------------------------
def create_response(content):
    """Create a simple HTTP response."""
    return f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode(FORMAT)

def read_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

#Webdirect--------------------------------------------------------------
def handle_http_request(request):
    """Handles HTTP requests."""
    request_line = request.split('\n')
    method, uri = request_line[0].split()[:2]
    authentic = request_line[4].split()[1]
    print(method, uri)
    if method == "GET":
        if uri == "/login" or uri == "/":
            return create_response(read_html("app/templates/login.html"))
        elif uri == "/home":
            return create_response(read_html("app/templates/home.html"))
        elif uri == "/register":
            return create_response(read_html("app/templates/register.html"))
    elif method == "POST":
        if uri == "/login":
            if "username=admin&password=admin" in request:
                return create_response(read_html("app/templates/home.html"))
            else:
                return create_response(read_html("app/templates/login.html"))
        elif uri == "/register":
            return create_response(read_html("app/templates/login.html"))
    else:
        return create_response(read_html("404.html"))

#Main--------------------------------------------------------------
def main(): 
    mainServer = createServerSocket()
    print("SERVER SIDE: ", HOST, " : ", SERVER_PORT)

    while True: 
        conn, addr = mainServer.accept()
        request = conn.recv(1024).decode(FORMAT)
        response = handle_http_request(request)
        conn.sendall(response)
    
    conn.close()
        
#Launch--------------------------------------------------------------
if __name__ == "__main__": 
    main()
    
