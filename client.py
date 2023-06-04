import socket
import sys
import os

import ast

# inisialisasi direktori client
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Client:
    def __init__(self, SERVER_HOST, SERVER_PORT) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (SERVER_HOST, SERVER_PORT)

        self.username = ""
        self.kewan = {}

    def get_client_host(self):
        return self.client_host
    
    def get_client_port(self):
        return self.client_port

    def connect(self):
        self.client_socket.connect(self.server_address)

    def client_send(self, msg):
        self.client_socket.send(msg.encode('utf-8'))

    def client_receive(self):
        msg = self.client_socket.recv(4096).decode('utf-8')
        return msg
    
    def set_username(self, username):
        self.username = username

    def get_username(self) -> str:
        return self.username
    
    def set_kewan(self, kewan):
        self.kewan = kewan

    def get_kewan(self) -> dict:
        return self.kewan

if __name__ == "__main__":
    # Player Info
    username = ""
    while username == "":
        username = input("Masukkan username: ")

    client = Client('127.0.0.1', 12345)
    client.connect()

    try:
        # send username info
        client.client_send(username)

        # get welcome message
        msg = client.client_receive()
        print(msg)

        # get room info / game start
        msg = client.client_receive()
        if msg == "Waiting for player...":
            print(msg)

            # get game start message
            msg = client.client_receive()
            print(msg)
            print("You are player I")

        # get game start message
        elif msg == "======== Game is starting! ========\n":
            print(msg)
            print("You are player II")

        # get list kewan
        msg = client.client_receive()
        kewan = input(msg)

        # send kewan till kewan is valid
        client.client_send(kewan)
        kewan_data = client.client_receive()
        while True:
            if(kewan_data == "Kewan tidak tersedia!\n\nMasukkan nama kewan: "):
                kewan = input(msg)
                client.client_send(kewan)
                kewan_data = client.client_receive()
            else:
                break

        # set kewan
        kewan_data = ast.literal_eval(kewan_data)
        print(kewan_data)
    
    except KeyboardInterrupt:
        client.client_socket.close()
        sys.exit(0)