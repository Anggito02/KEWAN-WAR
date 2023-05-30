import socket
import select
import sys

import os

import ast

'''
    GAME CONFIGURATION
'''
with open('character.txt', 'r') as f:
    data = f.read()

# save kewan dictionary
KEWAN = ast.literal_eval(data)
'''
    SERVER CONFIGURATION
'''

# inisialisasi base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# gunakan konfigurasi yang sudah dibuat
CONFIG_FILE = open(BASE_DIR + "/server.conf", "r")

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

server_address = (HOST, PORT)

# inisialisasi socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(2)

# List untuk menyimpan socket yang terhubung
input_socket = [server_socket]

try:
    # lakukan pengecekan koneksi dengan klien
    while True:
        socket_ready, _, _ = select.select(input_socket, [], [])

        for sock_r in socket_ready:
            # jika socket merukapan server socket, maka terima koneksi baru
            if sock_r == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

                print(f"Connection from {client_address} has been established!")

            # jika socket bukan merupakan server socket, maka terhubung dengan klien
            else:
                # terima hello message dari klien
                hello_msg = sock_r.recv(1024).decode("utf-8")
                print(hello_msg)

                # kirim welcome message ke klien
                sock_r.send("Welcome to Kewan War!".encode("utf-8"))

                '''
                    ROOM LOADING/PLATER LOADING LOGIC
                '''
                # buat thread baru

                # kirim list room ke klien

                # terima pilihan room dari klien

                # masukkan player ke room

                # jika room berisi 1 player
                # kirim pesan ke klien bahwa room sedang menunggu player

                # jika room berisi 2 player
                # lock room

                # kirim pesan ke klien bahwa room sudah terisi

                '''
                    GAME LOGIC
                '''

                # kirim game start ke klien
                sock_r.send("===== Game Start =====\n".encode("utf-8"))

                # dapatkan karakter player
                while True:
                    # terima nama kewan
                    nama_kewan = sock_r.recv(1024).decode("utf-8")

                    # kewan tidak ditemukan
                    if nama_kewan not in list(KEWAN.keys()):
                        sock_r.send("Kewan tidak ditemukan!\n".encode("utf-8"))
                        continue
                    else:
                        break
                
                player_kewan_detail = KEWAN[nama_kewan]
                print(type(player_kewan_detail))

                # kewan art format
                kewan_art = ""
                for elem in player_kewan_detail['art']:
                    kewan_art += elem + "\n"

                # kirim detail kewan ke klien
                kewan_info_format = f"{kewan_art}\n\n" \
                    f"Nama Kewan: {nama_kewan}\n" \
                    f"Health: {player_kewan_detail['health']}\n" \
                    f"Defense: {player_kewan_detail['defense']}\n\n" \
                    f"Basic Attack: {player_kewan_detail['b_attack']}\n" \
                    f"Skill 1: {player_kewan_detail['skill-1']['name']}\n" \
                    f"Skill 2: {player_kewan_detail['skill-2']['name']}\n" \
                    f"Ultimate: {player_kewan_detail['ultimate']['name']}\n"
                
                sock_r.send(kewan_info_format.encode("utf-8"))

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)