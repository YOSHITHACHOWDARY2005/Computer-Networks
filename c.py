import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.137.224', 8888))
print(" Connected to server on port 9999.")
while True:
    msg = input("Client: ")
    client_socket.send(msg.encode())
    if msg.lower() == 'exit':
        break
    reply = client_socket.recv(1024).decode() 
    print(f"Server: {reply}")
client_socket.close()