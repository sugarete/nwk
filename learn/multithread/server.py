import socket 
import threading

HOST = "192.168.1.6" 
SERVER_PORT = 8080
FORMAT = "utf8"

#Setup--------------------------------------------------------------

def clienthandler(conn, addr):
    print("conn:",conn.getsockname())

    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr, "says", msg)

    print("client ",addr, "disconnected")
    conn.close()

#Main--------------------------------------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")

nClients = 0
while (nClients < 3):
    try:
        conn, addr = s.accept()
        thr = threading.Thread(target=clienthandler, args=(conn, addr))
        #Khi main ket thuc thi thread cung ket thuc
        thr.daemon = True
        thr.start()
    except:
        print("Error")
    
    nClients += 1

print("End")
input()
s.close()


