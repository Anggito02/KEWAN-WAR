import game

if __name__ == "__main__":
    username = input("Masukkan username: ")
    g = game.Game(username)
    g.start_game()