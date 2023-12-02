# import pytube as yt
# import validators
import socket 
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
 
#YTprocess--------------------------------------------------------------
# def extract(url):
#     video = yt.YouTube(url)
#     url = video.streams.get_highest_resolution().url
#     return url

#Webprocess--------------------------------------------------------------
def direct(message):
    if message == "/":
        return "index.html"
    elif message == "/signin.html":
        return "signin.html"
    elif message == "/signup.html":
        return "signup.html"


# def create_response(content):


#Thread--------------------------------------------------------------
def clienthandler(conn, addr):
    print("conn:",conn.getsockname())
    msg = None
    msg = conn.recv(1024).decode()
    
    print(msg)
    # print(filename)
    # while(msg != "exit"):
    #     msg = conn.recv(1024).decode(FORMAT)
    #     print("client ",addr, "says", msg)
    #     if not validators.url(msg):
    #         conn.send("Invalid url, please type again".encode(FORMAT))
    #         print("client ",addr, "sent", msg)
    #         continue
    #     conn.send(extract(msg).encode(FORMAT))
    #     print("client ",addr, "sent", msg)

    print("client ",addr, "disconnected")
    conn.close()



#Main--------------------------------------------------------------
def main(): 
    mainServer = createServerSocket()
    print("SERVER SIDE: ", HOST, " : ", SERVER_PORT)
    print("Waiting for Client")
    nClients = 0
    while(nClients < 3): 
        try:
            conn, addr = mainServer.accept()
            thr = threading.Thread(target=clienthandler, args=(conn, addr))
            thr.daemon = True
            thr.start()
        except:
            print("Error")
        nClients += 1
    print("End")
    input()
    mainServer.close()

#Launch--------------------------------------------------------------
if __name__ == "__main__": 
    main()
    
