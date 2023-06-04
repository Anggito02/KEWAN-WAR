import os
import socket
import select
import sys
import threading

from GameRoom import GameRoom

import ast
from typing import List

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
    with open(os.path.join(BASE_DIR, "..", "config", "character.txt"), 'r') as f:
        data = f.read()

    global KEWAN_DATA
    KEWAN_DATA = ast.literal_eval(data)

'''
    ====================
'''

'''
    SERVER CONFIGURATION
'''
def get_config():
    global HOST, PORT

    # gunakan konfigurasi yang sudah dibuat
    CONFIG_FILE = open(os.path.join(BASE_DIR, "..", "config", "server.conf"), "r")

    # save config to variable
    for line in CONFIG_FILE:
        if line.startswith("PORT"):
            PORT = int(line.split("=")[1].strip())
        elif line.startswith("HOST"):
            HOST = (line.split("=")[1].strip())

    # tutup config file
    CONFIG_FILE.close()

'''
    ====================
'''

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

def server_send(socket_s: socket.socket, msg):
    socket_s.send(str(msg).encode("utf-8"))

def server_receive(socket_r):
    msg = socket_r.recv(2048).decode("utf-8")
    return msg

'''
    ====================
'''

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

        # set username to GameRoom
        room.set_player_username(client_socket, username)
    else:
        print("Player already exists!")
        server_send(client_socket, "Player already exists!")
    
    print("Room: ", room.get_id())
    print("Player: ")
    print(room.get_players_info())

    ''' ROOM WAITING '''
    if not room.is_room_ready():
        print("Waiting for player...")
        server_send(client_socket, "Waiting for player...")

    while True:
        if room.is_room_ready():
            break

    print("Game is starting!")
    server_send(client_socket, "======== Game is starting! ========\n")

    ''' KEWAN SELECTION '''
    # send kewan selection
    kewan_selection_format = f"Pilih Kewanmu!\n"

    iter = 1
    for kewan in list(KEWAN_DATA.keys()):
        kewan_selection_format += str(iter) + ". " + kewan + '\n'
        iter = iter + 1

    kewan_selection_format += '\n\nMasukkan nama kewan: '

    server_send(client_socket, kewan_selection_format)

    # get kewan selection
    kewan_selection = server_receive(client_socket)
    print(kewan_selection)

    # check kewan selection
    while kewan_selection not in list(KEWAN_DATA.keys()):
        server_send(client_socket, "Kewan tidak tersedia!\n\nMasukkan nama kewan: ")
        kewan_selection = server_receive(client_socket)

    # set kewan info in GameRoom
    room.set_player_kewan(client_socket, kewan_selection)

    # set kewan selection
    server_send(client_socket, KEWAN_DATA[kewan_selection])

    # check player ready
    server_receive(client_socket)
    room.set_player_ready(client_socket)

    if not room.is_game_ready():
        print("Waiting a player for choosing")
        server_send(client_socket, "Waiting for enemy choosing Kewan...")

    while True:
        if room.is_game_ready():
            break

    # send enemy kewan
    if client_socket == room.get_first_player_sock():
        kewan_2_name = room.get_player_kewan(room.get_second_player_sock())
        kewan_2_format = f"===== Musuhmu =====\n" \
                            f"Username: {room.get_player_username(room.get_second_player_sock())}\n" \
                            f"Kewan: {kewan_2_name}\n" \
        
        for lines in KEWAN_DATA[kewan_2_name]['art']:
            kewan_2_format += lines + '\n'

        kewan_2_format += '\n\n'

        print(kewan_2_format)
        server_send(client_socket, kewan_2_format)
    elif client_socket == room.get_first_player_sock():
        kewan_1_name = room.get_player_kewan(room.get_first_player_sock())
        kewan_1_format = f"===== Musuhmu =====\n" \
                            f"Username: {room.get_player_username(room.get_first_player_sock())}\n" \
                            f"Kewan: {kewan_1_name}\n" \
        
        for lines in KEWAN_DATA[kewan_1_name]['art']:
            kewan_1_format += lines + '\n'

        kewan_1_format += '\n\n'

        print(kewan_1_format)
        server_send(client_socket, kewan_1_format)

    # send game start message
    server_send(client_socket, "========== BATTLE START ==========")

    ''' GAME START '''

'''
    ====================
'''

'''
    MAIN PROGRAM
'''
if __name__ == "__main__":
    # inisialisasi KEWAN
    get_kewan()

    # inisialisasi config
    get_config()
    
    # inisialisasi server connection
    server_socket = server_connection()

    # lakukan pengecekan koneksi dengan klien
    try:
        while True:
            client_socket, client_address = server_socket.accept()
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
