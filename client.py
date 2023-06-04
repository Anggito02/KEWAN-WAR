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

    ''' CLIENT CONNECTION '''
    def get_client_host(self):
        return self.client_host
    
    def get_client_port(self):
        return self.client_port

    def connect(self):
        self.client_socket.connect(self.server_address)

    ''' CLIENT COMMUNICATION '''
    def client_send(self, msg):
        self.client_socket.send(msg.encode('utf-8'))

    def client_receive(self):
        msg = self.client_socket.recv(4096).decode('utf-8')
        return msg
    
    ''' CLIENT INFO '''
    def set_username(self, username):
        self.username = username

    def get_username(self) -> str:
        return self.username
    
    ''' KEWAN INFO '''
    def set_kewan(self, kewan):
        self.kewan = kewan

    def get_kewan_name(self) -> str:
        return str(self.kewan.keys())
    
    def get_kewan_health(self) -> int:
        return int(self.kewan['health'])
    
    def get_kewan_defense(self):
        return (int(self.kewan['defense']['min']), int(self.kewan['defense']['max']))
    
    def get_kewan_b_attack(self) -> int:
        return (int(self.kewan['b_attack']))
    
    def get_kewan_skill_1(self):
        return (self.kewan['skill-1']['name'], int(self.kewan['skill-1']['min']), int(self.kewan['skill-1']['max']))

    def get_kewan_skill_2(self):
        return (self.kewan['skill-2']['name'], int(self.kewan['skill-2']['min']), int(self.kewan['skill-2']['max']))
    
    def get_kewan_ulti(self):
        return (self.kewan['ultimate']['name'], int(self.kewan['ultimate']['min']), int(self.kewan['ultimate']['max']))
    
    def get_kewan_art(self):
        return self.kewan['art']

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
        client.set_kewan(kewan_data)

        print(f"======== {kewan} ========")
        print()
        for lines in client.get_kewan_art():
            print(lines)
        print()
        print()
        print(f"Health: {client.get_kewan_health()}")
        print(f"Defense: {client.get_kewan_defense()}")
        print()
        print()
        print(f"Basic Attack: {client.get_kewan_b_attack()}")
        print(f"Skill 1: {client.get_kewan_skill_1()}")
        print(f"Skill 2: {client.get_kewan_skill_2()}")
        print(f"Ultimate: {client.get_kewan_ulti()}")
        print()
        print()

        # client ready to play
        client.client_send("ready")

        # get waiting message / enemy kewan info
        msg = client.client_receive()
        if msg == "Waiting for enemy choosing Kewan...":
            print(msg)

            # get enemy kewan info
            msg = client.client_receive()
            print(msg)

            # get battle start message
            msg = client.client_receive()
            print(msg)
            print(f"Good luck {username}!\n\n")
        else:
            # print enemy kewan info
            print(msg)

            # get battle start message
            msg = client.client_receive()
            print(msg)
            print(f"Good luck {username}!\n\n")

        ''' GAME START '''

    except KeyboardInterrupt:
        client.client_socket.close()
        sys.exit(0)