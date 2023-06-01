import socket,select,sys, os, ast, threading
from typing import List
from GameRoom import GameRoom

# inisialisasi base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ServerGame:
    def __init__(self, HOST=None, PORT=None, GAMEROOM=None):
        self.host = HOST
        self.port = PORT
        self.GAME_ROOMS: List[GameRoom] = GAMEROOM
        self.server_address = (self.host, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_connection(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(10)
    
    def server_send(self,client_socket,msg):
        client_socket.send(msg.encode("utf-8"))

    def server_receive(self,client_socket):
        msg = client_socket.recv(1024).decode("utf-8")
        return msg
    def start(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} has been established!")
                if len(self.GAME_ROOMS) == 0 or len(self.GAME_ROOMS[-1].players) == 2:
                    new_room = GameRoom()
                    self.GAME_ROOMS.append(new_room)
                else:
                    new_room = self.GAME_ROOMS[-1]
                # start thread
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,new_room))
                client_thread.start()
        except KeyboardInterrupt:
            self.server_socket.close()
            sys.exit(0)

    def handle_client(self, client_socket, room: GameRoom):
        while not room.is_game_ready():
            if room.add_player(client_socket):
                print("Player added!")
                # get client username
                username = self.server_receive(client_socket)
                # send welcome message
                self.server_send(client_socket, f"Welcome, {username}!")
            else:
                print("Player already exists!")
                self.server_send(client_socket, "Player already exists!")

            ''' ROOM WAITING '''
            if not room.is_game_ready():
                print("Waiting for player...")
                self.server_send(client_socket, "Waiting for player...")
            
            if room.is_game_ready():
                break
        print("Room: ", room.get_id())
        print("Player: ")
        print(room.get_players())
        print("Game is starting!")
        while True:
            data = self.server_receive(client_socket)
            if not data:
                self.server_send(client_socket,"Goodbye")
                continue
            if data in KEWAN_DATA:
                player_kewan_detail = KEWAN_DATA[data]
                # kewan art format
                kewan_art = ""
                for elem in player_kewan_detail['art']:
                    kewan_art += elem + "\n"
                # kirim detail kewan ke klien
                kewan_info_format = f"{kewan_art}\n\n" \
                    f"Nama Kewan: {data}\n" \
                    f"Health: {player_kewan_detail['health']}\n" \
                    f"Defense: {player_kewan_detail['defense']}\n\n" \
                    f"Basic Attack: {player_kewan_detail['b_attack']}\n" \
                    f"Skill 1: {player_kewan_detail['skill-1']['name']}\n" \
                    f"Skill 2: {player_kewan_detail['skill-2']['name']}\n" \
                    f"Ultimate: {player_kewan_detail['ultimate']['name']}\n"
                self.server_send(client_socket,kewan_info_format)

if __name__ == "__main__":

    with open(os.path.join(BASE_DIR, "config", "character.txt"), 'r') as f:
        data = f.read()

    KEWAN_DATA = ast.literal_eval(data)
    # inisialisasi config
    CONFIG_FILE = open(os.path.join(BASE_DIR, "config", "server.conf"), "r")

    # save config to variable
    for line in CONFIG_FILE:
        if line.startswith("PORT"):
            PORT = int(line.split("=")[1].strip())
        elif line.startswith("HOST"):
            HOST = (line.split("=")[1].strip())

    # tutup config file
    CONFIG_FILE.close()

    print(type(KEWAN_DATA))
    serverGame = ServerGame(HOST,int(PORT),[])
    serverGame.server_connection()
    serverGame.start()
