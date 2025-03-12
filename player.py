from enum import Enum
from utils import generate_response
import prompt 
class Role(Enum):
    DEFAULT = 0
    WEREWOLF = 1
    VILLAGER = 2
    WITCH = 3
    SEER = 4
    HUNTER = 5

class Player:
    
    def __init__(self, player_no:int):
        self.player_no = player_no
        self.role = Role.DEFAULT
        self.alive = True
        self.private_message = []
    def __repr__(self):
        return f"Player {self.player_no}(Alive: {self.alive})"
    
    def __str__(self):
        return f"Player {self.player_no}(Alive: {self.alive})"
    
    def action(self,game_history,player_alive, **kwargsargs):
        if self.role == Role.WEREWOLF:
            return self.wolf_action(game_history,player_alive,kwargsargs["vote_history"])
        if self.role == Role.WITCH:
            return self.witch_action(game_history,player_alive,kwargsargs["player_killed"],kwargsargs["num_antidote"],kwargsargs["num_poison"])
        if self.role == Role.SEER:
            return self.seer_action(game_history,player_alive)
        if self.role == Role.HUNTER:
            return self.hunter_action(game_history,player_alive)
        
    def speech(self,game_history,messages):
        raise NotImplementedError
        return ""
    
    def vote(self,game_history,messages,candidates):
        raise NotImplementedError
        return 0