import game

if __name__ == "__main__":
    username = input("Masukkan username: ")
    g = game.Game(username=username)
    while True:
        command = input("Berikan Command(Angka Saja):\
                        \n1. Start\
                        \n2. Set KEWAN\n")
        if command == "1":
            g.start_game()
        elif command == "2":
            g.set_kewan()