from pytube import YouTube
import socket, os, threading
from urllib.parse import unquote
import login as login
import register as register

#Setup--------------------------------------------------------------
HOST = "0.0.0.0"
SERVER_PORT = 8080
FORMAT = "utf8"

def createServerSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, SERVER_PORT))
    s.listen()
    return s

download_directory = 'downloaded_videos'
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

#Authentication---------------------------------------------------------


#YoutubeProcessing------------------------------------------------------
def youtubeProcessing(request):
    url = request.split("url=")[1].split(" ")[0]
    url = unquote(url)
    print("Downloading video at: ", url)
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video_path = video.download(download_directory)
    return video_path

def createVideoResponse(video_path):
    with open (video_path, "rb") as f:
        video_content = f.read()
    response = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Disposition: attachment; filename={os.path.basename(video_path)}\r\n"
        f"Content-Type: video/mp4\r\n"
        f"Content-Length: {len(video_content)}\r\n\r\n"
    ).encode(FORMAT) + video_content
    return response

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
        1: "Account is already registered. Please Sign in."
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
    """Handles HTTP requests."""
    request_line = request.split('\n')
    method, uri = request_line[0].split()[:2]
    print("client addr ", addr, "with request: ", method, uri)
    if method == "GET":
        if uri == "/login" or uri == "/":
            return create_response(read_html("app/templates/login.html"))
        elif uri == "/register":
            return create_response(read_html("app/templates/register.html"))
        else :
            return create_response(read_html("app/templates/404.html"))
    elif method == "POST":
        if uri == "/":
            logstring = request.splitlines()[-1]
            check = login.checkLogin(logstring)
            if check == 0:    
                return create_response(read_html("app/templates/home.html") + ErrorLoginResponse(check))
            else:
                return create_response(read_html("app/templates/login.html") + ErrorLoginResponse(check))
        elif uri == "/register":
            check = register.register_handle(request)
            if check == 0:
                return create_response(read_html("app/templates/login.html") + ErrorRegisterResponse(check))
            else :
                return create_response(read_html("app/templates/register.html") + ErrorRegisterResponse(check))
        elif uri == "/submit-url":
            return createVideoResponse(youtubeProcessing(request))
        else :
            return create_response(read_html("app/templates/404.html"))
    else:
        return create_response(read_html("app/templates/404.html")) 

#Multithreading----------------------------------------------------
def clientHandler(conn, addr):
    request = conn.recv(1024).decode(FORMAT)
    if request != "":
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

    print("End")
    mainServer.close()

#Launch--------------------------------------------------------------
if __name__ == "__main__": 
    main()
    
