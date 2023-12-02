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
    while (msg != "exit"):
        msg = input("talk: ")
        client.sendall(msg.encode(FORMAT))
        print("Server response:")
        print(client.recv(1024).decode(FORMAT))

except:
    print("Error")



input()
client.close()