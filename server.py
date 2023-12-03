import socket, threading
import login as login
import register as account
import yt as yt

#Setup--------------------------------------------------------------
HOST = "0.0.0.0"
SERVER_PORT = 8080
FORMAT = "utf8"

def createServerSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, SERVER_PORT))
    s.listen()
    return s

#ScriptMessage--------------------------------------------------------------
def ErrorLoginResponse(status):
    messages = {
        0: "Login successfully.",
        1: "Incorrect username or password. Please try again.",
        2: "Username is not available. Please Register.",
    }
    msg = messages.get(status, "Unknown error")
    return f'<script>alert("{msg}");</script>'

def ErrorRegisterResponse(status):
    messages = {
        0: "Register successfully.",
        1: "Password is not long enough (>5 words). Please try again.",
        2: "Account is already registered. Please Sign in."
    }
    msg = messages.get(status, "Unknown error")
    return f'<script>alert("{msg}");</script>'

def ErrorChangePwdResponse(status):
    messages = {
        0: "Change password successfully.",
        1: "Password is not long enough (>5 words). Please try again.",
        2: "Incorrect username or password. Please try again.",
    }
    msg = messages.get(status, "Unknown error")
    return f'<script>alert("{msg}");</script>'

#RenderHTML--------------------------------------------------------------
def create_response(content):
    """Create a simple HTTP response."""
    return f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode(FORMAT)

def read_html(file_path):
    with open(file_path, "r") as f:
        return f.read()

#Webdirect--------------------------------------------------------------
def handle_http_request(addr, request):
    # Extract the required information from the given request.
    request_line = request.split('\n')
    method, uri = request_line[0].split()[:2]
    print("client addr ", addr, "with request: ", method, uri)
    # Handles HTTP GET requests.Load Page
    if method == "GET":
        if uri == "/login" or uri == "/":
            return create_response(read_html("app/templates/login.html"))
        elif uri == "/register":
            return create_response(read_html("app/templates/register.html"))
        elif uri == "/cpwd":
            return create_response(read_html("app/templates/cpwd.html"))
        elif uri.startswith("/videos/"):
            return yt.createVideoResponse(yt.handle_video_request(request))
        elif uri == "/home":
            return create_response(read_html("app/templates/home.html"))
        elif uri == "/vidlist":
            video_list = yt.list_videos()
            return create_response(read_html("app/templates/vidlist.html") + video_list)
        else :
            return create_response(read_html("app/templates/404.html"))
    # Handles HTTP POST requests.Register, Signin, Download
    elif method == "POST":
        if uri == "/submit-url":
            return yt.createVideoResponse(yt.youtubeProcessing(request))
        elif uri == "/":
            logstring = request.splitlines()[-1]
            check = login.checkLogin(logstring)
            if check == 0:    
                return create_response(read_html("app/templates/home.html") + ErrorLoginResponse(check))
            else:
                return create_response(read_html("app/templates/login.html") + ErrorLoginResponse(check))
        elif uri == "/register":
            check = account.register_handle(request)
            if check == 0:
                return create_response(read_html("app/templates/login.html") + ErrorRegisterResponse(check))
            else :
                return create_response(read_html("app/templates/register.html") + ErrorRegisterResponse(check))
        elif uri == "/cpwd":
            check = account.change_pwd(request)
            if check == 0:
                return create_response(read_html("app/templates/login.html") + ErrorChangePwdResponse(check))
            else :
                return create_response(read_html("app/templates/cpwd.html") + ErrorChangePwdResponse(check))
        else :
            return create_response(read_html("app/templates/404.html"))
    else:
        return create_response(read_html("app/templates/404.html")) 

#Multithreading----------------------------------------------------
def clientHandler(conn, addr):
    request = conn.recv(1024).decode(FORMAT)
    if request != "":
        print("client addr ", addr, "with request: ", request)
        response = handle_http_request(addr, request)
        conn.sendall(response)
    conn.close()

#Main--------------------------------------------------------------
def main(): 
    mainServer = createServerSocket()
    print("SERVER SIDE: ", HOST, " : ", SERVER_PORT)
    try:
        while True: 
            conn, addr = mainServer.accept()
            thr = threading.Thread(target=clientHandler, args=(conn, addr))
            thr.daemon = True
            thr.start() 

    except KeyboardInterrupt:
        print("Shutting down the server...")
        mainServer.close()

#Launch--------------------------------------------------------------
if __name__ == "__main__": 
    main()
    
