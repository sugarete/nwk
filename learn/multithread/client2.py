import socket

HOST = "192.168.1.6"
SERVER_PORT = 8080
FORMAT = "utf8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")


try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())
    msg = None
    while (msg != "x"):
        msg = input("talk: ")
        client.sendall(msg.encode(FORMAT))

except:
    print("Error")



input()
client.close()