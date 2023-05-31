import socket

from typing import List
import datetime

class GameRoom:
    def __init__(self) -> None:
        self.players: List[socket.socket] = []
        self.id = self.generate_id()
        self.is_game_over = False
    
    def generate_id(self) -> None:
        now = datetime.now()
        id = now.strftime("%d%m%Y%H%M%S")
        return id

    def add_player(self, player) -> bool:
        if len(self.players) < 2:
            self.players.append(player)
            return True
        else:
            return False
        
    def remove_player(self, player) -> None:
        if player in self.players:
            self.players.remove(player)
        
    def destroy_room(self) -> None:
        self.players = []
        self.is_game_over = True

