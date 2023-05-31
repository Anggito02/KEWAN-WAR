import socket
import sys
import os

# inisialisasi direktori client
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# inisialisasi koneksi server
server_address = ('localhost', 12345)

# inisialisasi socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# kirim data ke server
try:
    while True:
        # kirim hello server
        hello_msg = "Hello Server!\n" + client_socket.getsockname()[0] + " : " + str(client_socket.getsockname()[1])
        client_socket.send(hello_msg.encode('utf-8'))

        # terima game start dari server
        welcome_game_msg = client_socket.recv(1024).decode('utf-8')
        print(welcome_game_msg)

        # terima list room dari server

        # pilih room

        # kirim pilihan room ke server

        # terima game start dari server
        game_start_msg = client_socket.recv(1024).decode('utf-8')
        print(game_start_msg)

        # pilih kewan
        while True:
            # minta nama kewan pada player
            kewan_nama = input("Pilih kewan (Masukkan nama):\
                \n1. Trippi\
                \n2. SoniLandak\
                \n3. Burhan\
                \n4. Cython\
                \n5. Bhaanther\n")
            
            # kirim nama kewan ke server
            client_socket.send(kewan_nama.encode('utf-8'))

            # terima pesan dari server
            kewan_info = client_socket.recv(1024).decode('utf-8')
            
            # kewan tidak ditemukan
            if kewan_info == "Kewan tidak ditemukan!\n":
                print(kewan_info)
                continue
            else:
                break

        # print info kewan
        print(kewan_info)

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)