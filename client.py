import socket
import sys
import os

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
        msg = self.client_socket.recv(1024).decode('utf-8')
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
    client = Client('127.0.0.1', 12345)
    client.connect()

    try:
        while True:
            # get welcome message
            msg = client.client_receive()
            print(msg)
    
    except KeyboardInterrupt:
        client.client_socket.close()
        sys.exit(0)