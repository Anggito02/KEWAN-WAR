import socket

from typing import List
import datetime

class GameRoom:
    def __init__(self) -> None:
        self.players: List[socket.socket] = []
        self.id = self.generate_id()
        self.is_game_over = False

        self.player1 = {
            "username": "",
            "ready": False,
            "turn": True,

            "kewan_name": "",
            "kewan_health": int
        }

        self.player2 = {
            "username": "",
            "ready": False,
            "turn": False,

            "kewan_name": "",
            "kewan_health": int
        }
    
    ''' ROOM CONFIGURATION '''
    def generate_id(self) -> None:
        now = datetime.datetime.now()
        id = now.strftime("%d%m%Y%H%M%S")
        return id
    
    def get_id(self) -> str:
        return self.id
    
    def is_room_ready(self) -> bool:
        if len(self.players) == 2:
            return True
        else:
            return False
        
    def destroy_room(self) -> None:
        self.players = []
        self.is_game_over = True

    ''' PLAYER CONFIGURATION '''
    def add_player(self, player) -> bool:
        if len(self.players) < 2:
            self.players.append(player)
            return True
        else:
            return False
        
    def remove_player(self, player) -> None:
        if player in self.players:
            self.players.remove(player)
        
    def get_players_info(self) -> str:
        players = ""
        for player in self.players:
            players += f"{player.getpeername()[0]} {player.getpeername()[1]}\n"
        return players
    
    def get_first_player_sock(self) -> socket.socket:
        return self.players[0]
    
    def get_second_player_sock(self) -> socket.socket:
        return self.players[1]
    
    def set_player_username(self, client_socket, username) -> None:
        if client_socket == self.players[0]:
            self.player1['username'] = username
        else:
            self.player2['username'] = username

    def get_player_username(self, client_socket) -> str:
        if client_socket == self.players[0]:
            return self.player1['username']
        else:
            return self.player2['username']
        
    def set_player_kewan(self, client_socket, kewan_name) -> None:
        if client_socket == self.players[0]:
            self.player1['kewan_name'] = kewan_name
        else:
            self.player2['kewan_name'] = kewan_name

    def get_player_kewan(self, client_socket) -> dict:
        if client_socket == self.players[0]:
            return self.player1['kewan_name']
        else:
            return self.player2['kewan_name']
        
    def set_player_ready(self, client_socket) -> None:
        if client_socket == self.players[0]:
            self.player1['ready'] = True
        else:
            self.player2['ready'] = True

    ''' GAME CONFIGURATION '''
    def is_game_ready(self) -> bool:
        if self.player1['ready'] and self.player2['ready']:
            return True
        else:
            return False
        
    def get_turn(self):
        if self.player1['turn']:
            return (self.players[0], self.players[1])
        else:
            return (self.players[1], self.players[0])
        
    def give_damage(self, client_socket, damage) -> None:
        if client_socket == self.players[0]:
            self.player2['kewan_health'] -= damage
        else:
            self.player1['kewan_health'] -= damage

    def check_health_status(self) -> bool:
        if self.player1['kewan_health'] <= 0 or self.player2['kewan_health'] <= 0:
            return True
        else:
            return False
            
    def change_turn(self):
        self.player1['turn'] = not self.player1['turn']
        self.player2['turn'] = not self.player2['turn']