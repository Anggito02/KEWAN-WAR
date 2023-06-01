import socket, sys
class Connection:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 12345
        self.addr = (self.host, self.port)
        self.data_kewan = None

    def connect(self):
        self.client_socket.connect(self.addr)

    def send(self, cmd=None, data=None):
        try:
            if cmd == "Start":
                print(data)
                self.client_socket.send(data.encode('utf-8'))
            elif cmd == "SetKewan":
                while True:
                    # minta nama kewan pada player
                    kewan_nama = input("Pilih kewan (Masukkan nama):\
                        \n1. Trippi\
                        \n2. SoniLandak\
                        \n3. Burhan\
                        \n4. Cython\
                        \n5. Bhaanther\n")
                    
                    # kirim nama kewan ke server
                    self.client_socket.send(kewan_nama.encode('utf-8'))
                    # terima pesan dari server
                    kewan_info = self.client_socket.recv(1024).decode('utf-8')
                    
                    # kewan tidak ditemukan
                    if kewan_info == "Kewan tidak ditemukan!\n":
                        print(kewan_info)
                        continue
                    else:
                        break
                # print info kewan
                self.data_kewan = kewan_info
        except KeyboardInterrupt:
            self.client_socket.close()
            sys.exit(0)