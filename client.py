import socket
import sys
import os

import ast
import random

# inisialisasi direktori client
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Client:
    def __init__(self, SERVER_HOST, SERVER_PORT) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (SERVER_HOST, SERVER_PORT)

        self.username = ""
        self.kewan_name = ""
        self.kewan = {}

        self.enemy_username = ""
        self.enemy_kewan_name = ""
        self.enemy_defense = []

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

    def set_health(self, health):
        self.kewan['health'] = health

    def set_kewan_name(self, name):
        self.kewan_name = name

    def get_kewan_name(self) -> str:
        return self.kewan_name
    
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
    
    ''' ENEMY INFO '''
    def set_enemy(self, enemy):
        self.enemy_username = enemy[0]
        self.enemy_kewan_name = enemy[1]
        self.enemy_defense = enemy[2]

    def get_enemy_username(self) -> str:
        return self.enemy_username
    
    def get_enemy_kewan_name(self) -> str:
        return self.enemy_kewan_name

if __name__ == "__main__":
    # Player Info
    username = ""
    while username == "":
        username = input("Masukkan username: ")

    # Client Connection
    CONFIG_FILE = os.path.join(BASE_DIR, 'connection.conf')

    with(open(CONFIG_FILE, 'r')) as f:
        SERVER_HOST = f.readline().split("=")[1].strip()
        SERVER_PORT = int(f.readline().split("=")[1].strip())

    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect()

    try:
        # send username info
        client.client_send(username)
        client.set_username(username)

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
        elif msg == "======== Game is starting! ========":
            print(msg)
            print()
            print("You are player II")

        # get list kewan
        msg = client.client_receive()
        kewan = input(msg)

        # send kewan till kewan is valid
        client.client_send(kewan)
        kewan_data = client.client_receive()
        while True:
            if(kewan_data == "Kewan tidak tersedia!\n\nMasukkan nama kewan: "):
                while True:
                    kewan = input(msg)
                    if kewan != "":
                        break
                client.client_send(kewan)
                kewan_data = client.client_receive()
            else:
                client.set_kewan_name(kewan)
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

            enemy_username = msg.split('Username: ')[1].split('\n')[0]
            enemy_kewan_name = msg.split('Kewan: ')[1].split('\n')[0]
            enemy_defense = []
            enemy_defense.append(int(msg.split('Defense: ')[1].split('\n')[0].split(',')[0]))
            enemy_defense.append(int(msg.split('Defense: ')[1].split('\n')[0].split(',')[1]))

            client.set_enemy((enemy_username, enemy_kewan_name, enemy_defense))

            # get battle start message
            msg = client.client_receive()
            print(msg)
            print(f"Good luck {username}!\n\n")
            client.client_send('ready')
        else:
            # print enemy kewan info
            print(msg)

            enemy_username = msg.split('Username: ')[1].split('\n')[0]
            enemy_kewan_name = msg.split('Kewan: ')[1].split('\n')[0]
            enemy_defense = []
            enemy_defense.append(int(msg.split('Defense: ')[1].split('\n')[0].split(',')[0]))
            enemy_defense.append(int(msg.split('Defense: ')[1].split('\n')[0].split(',')[1]))

            client.set_enemy((enemy_username, enemy_kewan_name, enemy_defense))

            # get battle start message
            msg = client.client_receive()
            print(msg)
            print(f"Good luck {username}!\n\n")
            client.client_send('ready')

        ''' GAME START '''
        while True:
            msg = client.client_receive()
            if msg == "Game Over! You Win!":
                # print kewan state
                print(f"======== {client.get_kewan_name()} ========")
                print()
                for lines in client.get_kewan_art():
                    print(lines)
                print()
                print()
                print(f"Health: {client.get_kewan_health()}")
                print()
                print()

                print(f"{msg}\n{client.get_kewan_name()}'s {client.get_username()} berhasil mengalahkan {client.get_enemy_kewan_name()}!")
                print(f"{client.get_username()} berhasil memenangkan pertarungan melawan {client.get_enemy_username()}!\n")
                print(f"======== Terimakasih telah bermain! ========\n")
                quit = ""
                while(True):
                    quit = input("Please type 'y' or 'YES' to quit: ")
                    if quit == 'y' or quit == 'YES':
                        break
                
                break
            else:
                # get player turn
                if msg == "Giliranmu!":
                    print(msg)
                    print()

                    # get player action
                    while(True):
                        get_action_format = f"Serangan {client.get_kewan_name()}:\n1. Basic Attack\n2. Random Skill\n\nMasukkan nomor aksi: "
                        action = input(get_action_format)

                        if action == "1" or action == "2":
                            break
                        else:
                            print("Aksi tidak valid!\n")

                    # process action
                    if action == "1":
                        skill_name = "Basic Attack"
                        damage = client.get_kewan_b_attack()
                    elif action == "2":
                        rand_skill = random.randint(1, 3)                
                        if rand_skill == 1:
                            skill_name = client.get_kewan_skill_1()[0]
                            damage = random.randint(client.get_kewan_skill_1()[1], client.get_kewan_skill_1()[2])
                        elif rand_skill == 2:
                            skill_name = client.get_kewan_skill_2()[0]
                            damage = random.randint(client.get_kewan_skill_2()[1], client.get_kewan_skill_2()[2])
                        elif rand_skill == 3:
                            skill_name = client.get_kewan_ulti()[0]
                            damage = random.randint(client.get_kewan_ulti()[1], client.get_kewan_ulti()[2])

                    enemy_defense = random.randint(client.enemy_defense[0], client.enemy_defense[1])
                    damage = damage - enemy_defense

                    if damage < 0:
                        damage = 0

                    # user action info
                    print(f"{client.get_kewan_name()} menggunakan {skill_name} dan memberikan damage {damage} kepada {client.enemy_username}'s {client.enemy_kewan_name}!")

                    # send action to server
                    client.client_send(skill_name + "," + str(damage))

                elif msg == "Giliran musuhmu!":
                    # wait for enemy action
                    print(msg)
                    print()

                    # get enemy damage / game end
                    msg = client.client_receive()
                    if msg.startswith("Game Over! You Lose!"):
                        # print(msg)
                        over, action_name, damage_given = msg.split(",")
                        print(f"{client.enemy_username}'s {client.enemy_kewan_name} menggunakan {action_name} dan memberikan damage {damage_given} kepada {client.get_kewan_name()}!")

                        # set health to 0
                        client.set_health(0)

                        # print kewan state
                        print(f"======== {client.get_kewan_name()} ========")
                        print()
                        for lines in client.get_kewan_art():
                            print(lines)
                        print()
                        print()
                        print(f"Health: {client.get_kewan_health()}")
                        print()
                        print()

                        print(f"{over}\n{client.get_kewan_name()}'s {client.get_username()} gagal mengalahkan {client.get_enemy_kewan_name()}!")
                        print(f"{client.get_username()} gagal memenangkan pertarungan melawan {client.get_enemy_username()}!\n")
                        print("Coba lagi lain kali! Semangat!\n")
                        print(f"======== Terimakasih telah bermain! ========\n")
                        quit = ""
                        while(True):
                            quit = input("Please type 'y' or 'YES' to quit: ")
                            if quit == 'y' or quit == 'YES':
                                break
                        break
                    else:
                        dmg_given = msg
                        action_name, damage_given = dmg_given.split(",")
                        print(f"{client.enemy_username}'s {client.enemy_kewan_name} menggunakan {action_name} dan memberikan damage {damage_given} kepada {client.get_kewan_name()}!")

                        # set kewan health
                        client.set_health(client.get_kewan_health() - int(damage_given))

                        # print kewan new state
                        print(f"======== {client.get_kewan_name()} ========")
                        print()
                        for lines in client.get_kewan_art():
                            print(lines)
                        print()
                        print()
                        print(f"Health: {client.get_kewan_health()}")
                        print()

    except KeyboardInterrupt:
        client.client_socket.close()
        sys.exit(0)