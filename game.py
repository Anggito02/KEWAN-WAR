from connection import Connection
import re, sys

class Player():
    def __init__(self, username):
        self.connection = Connection()
        self.kewan_name = None
        self.health = None
        self.defense = None
        self.b_attack = None
        self.s1 = None
        self.s2 = None
        self.ult = None
        self.art = None
        self.username = username
    def set_kewanName(self, kewan_name):
        self.kewan_name = kewan_name
    def set_health(self, health):
        self.health = health
    def set_defense(self, defense):
        self.defense = defense
    def set_b_attack(self, b_attack):
        self.b_attack = b_attack
    def set_skill1(self, skill1):
        self.skill1 = skill1
    def set_skill2(self, skill2):
        self.skill2 = skill2
    def set_ult(self, ult):
        self.ult = ult
    def set_art(self, art):
        self.art = art
    
    def get_username(self):
        return self.username

class Game():
    def __init__(self, username):
        self.connection = Connection()
        self.player = Player(username)
        self.data_player = None
    def start_game(self):
        self.connection.connect()
        try:
            while True:
                cmd = input("Input command \
                            \n1.Start\
                            \n2.SetKewan\n\n")
                if cmd == "Start":
                    self.connection.send(cmd,self.player.get_username())
                elif cmd == "SetKewan":
                    self.connection.send(cmd)
                    self.data_player = self.connection.data_kewan
                    print(self.data_player)
                    self.SetKewaN()
                else:
                    print("Command Tidak ditemukan!")
                    continue
                respond = self.connection.get_client_socket().recv(1024).decode('utf-8')
                print(respond)
        except KeyboardInterrupt:
            self.client_socket.close()
            sys.exit(0)

    def SetKewaN(self):
        # ascii_art_match = re.search(r"ASCII ART: (.+)", self.data_player)
        # ascii_art  = ascii_art_match.group(1)
                
        nama_kewan_match = re.search(r"Nama Kewan: (.+)", self.data_player)
        self.player.set_kewanName(nama_kewan_match.group(1))

        # Extracting Health
        health_match = re.search(r"Health: (.+)", self.data_player)
        self.player.set_health(health_match.group(1))

        # Extracting Defense
        defense_match = re.search(r"Defense: (.+)", self.data_player)
        self.player.set_defense(defense_match.group(1))

        # Extracting Basic Attack
        basic_attack_match = re.search(r"Basic Attack: (.+)", self.data_player)
        self.player.set_b_attack(basic_attack_match.group(1))

        # Extracting Skill 1
        skill_1_match = re.search(r"Skill 1: (.+)", self.data_player)
        self.player.set_skill1(skill_1_match.group(1))

        # Extracting Skill 2
        skill_2_match = re.search(r"Skill 2: (.+)", self.data_player)
        self.player.set_skill2(skill_2_match.group(1))

        # Extracting Ultimate
        ultimate_match = re.search(r"Ultimate: (.+)", self.data_player)
        self.player.set_ult(ultimate_match.group(1))