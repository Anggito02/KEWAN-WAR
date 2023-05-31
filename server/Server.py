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

'''
    GAME CONFIGURATION
'''
def get_kewan():
    with open('../config/character.txt', 'r') as f:
        data = f.read()
    KEWAN_DATA = ast.literal_eval(data)

'''
    ====================
'''

'''
    SERVER CONFIGURATION
'''
def get_config():
    # inisialisasi base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # gunakan konfigurasi yang sudah dibuat
    CONFIG_FILE = open(BASE_DIR + "../config/server.conf", "r")

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
    server_addreass = (HOST, PORT)

    # inisialisasi socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_addreass)
    server_socket.listen(10)

    # List untuk menyimpan socket yang terhubung
    input_socket = [server_socket]

    return server_socket, input_socket

def server_send(socket_s, msg):
    socket_s.send(msg.encode("utf-8"))

def server_receive(socket_r):
    msg = socket_r.recv(1024).decode("utf-8")
    return msg

'''
    ====================
'''

'''
    GAME LOGIC
'''
def handle_client(client_socket, room: GameRoom):
    room.add_player(client_socket)
    print("Room: ", room.id)
    print("Player: ", room.players)

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
    server_socket, input_socket = server_connection()

    # lakukan pengecekan koneksi dengan klien
    try:
        while True:
            socket_ready, _, _ = select.select(input_socket, [], [])

            for sock_r in socket_ready:
                # jika socket merukapan server socket, maka terima koneksi baru
                if sock_r == server_socket:
                    client_socket, client_address = server_socket.accept()
                    input_socket.append(client_socket)

                # jika bukan server socket, maka terima pesan dari klien
                else:
                    if len(GAME_ROOMS) == 0 or len(GAME_ROOMS[-1].players) == 2:
                        new_room = GameRoom()
                        GAME_ROOMS.append(new_room)
                    else:
                        new_room = GAME_ROOMS[-1]

                    # start thread
                    client_thread = threading.Thread(target=handle_client, args=(sock_r, new_room))
                    client_thread.start()
    
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit(0)
