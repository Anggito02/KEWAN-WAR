import socket,select,sys, os, ast, threading
from typing import List
from GameRoom import GameRoom

HOST = ''
PORT = ''
KEWAN_DATA = {}
GAME_ROOMS: List[GameRoom] = []

# inisialisasi base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
    GAME CONFIGURATION
'''
def get_kewan():
    with open(os.path.join(BASE_DIR, "config", "character.txt"), 'r') as f:
        data = f.read()

    global KEWAN_DATA
    KEWAN_DATA = ast.literal_eval(data)

'''
    SERVER CONFIGURATION
'''
def get_config():
    global HOST, PORT

    # gunakan konfigurasi yang sudah dibuat
    CONFIG_FILE = open(os.path.join(BASE_DIR, "config", "server.conf"), "r")

    # save config to variable
    for line in CONFIG_FILE:
        if line.startswith("PORT"):
            PORT = int(line.split("=")[1].strip())
        elif line.startswith("HOST"):
            HOST = (line.split("=")[1].strip())

    # tutup config file
    CONFIG_FILE.close()

'''
    SERVER CONNECTION
'''
def server_connection():
    server_address = (HOST, PORT)

    # inisialisasi socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(10)

    return server_socket

def server_send(socket_s, msg):
    socket_s.send(msg.encode("utf-8"))

def server_receive(socket_r):
    msg = socket_r.recv(1024).decode("utf-8")
    return msg

'''
    GAME LOGIC
'''
def handle_client(client_socket, room: GameRoom):
    if room.add_player(client_socket):
        print("Player added!")

        # get client username
        username = server_receive(client_socket)

        # send welcome message
        server_send(client_socket, f"Welcome, {username}!")
    else:
        print("Player already exists!")
        server_send(client_socket, "Player already exists!")
    
    print("Room: ", room.get_id())
    print("Player: ")
    print(room.get_players())

    ''' ROOM WAITING '''
    if not room.is_game_ready():
        print("Waiting for player...")
        server_send(client_socket, "Waiting for player...")

    while True:
        if room.is_game_ready():
            break

    print("Game is starting!")

    ''' KEWAN SELECTION '''
    # send kewan selection
    kewan_selection_format = f"Pilih Kewanmu!\n"

    iter = 1
    for kewan in list(KEWAN_DATA.keys()):
        kewan_selection_format += str(iter) + ". " + kewan + '\n'
        iter = iter + 1

    kewan_selection_format += '\n\nMasukkan nama kewan: '

    server_send(client_socket, kewan_selection_format)

if __name__ == "__main__":
    # inisialisasi KEWAN
    get_kewan()

    # inisialisasi config
    get_config()

    server_socket = server_connection()
    # lakukan pengecekan koneksi dengan klien
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established!")
            
            if len(GAME_ROOMS) == 0 or len(GAME_ROOMS[-1].players) == 2:
                new_room = GameRoom()
                GAME_ROOMS.append(new_room)
            else:
                new_room = GAME_ROOMS[-1]

            # start thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, new_room))
            client_thread.start()
    
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)