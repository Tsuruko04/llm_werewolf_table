import random
import os
from player import Player, Role
class Game:
    def __init__(self):
        players = [Player(i) for i in range(1,10)]
        shuffled = random.sample(players,len(players))
        self.wolves = shuffled[:3]
        for wolf in self.wolves:
            wolf.role = Role.WEREWOLF
        self.villagers = shuffled[3:6]
        for villager in self.villagers:
            villager.role = Role.VILLAGER
        self.witch = shuffled[6]
        self.witch.role = Role.WITCH
        self.num_antidote = 1
        self.num_poison = 1
        self.seer = shuffled[7]
        self.seer.role = Role.SEER
        self.hunter = shuffled[8]
        self.hunter.role = Role.HUNTER
        self.game_history = []

    def game_set(self):
        """
        Stats the game
        """
        print("Game Over")
        with open("game_history.txt","w") as f:
            f.write("\n".join(self.game_history))
        exit(0)
    
    def get_alive_player_no(self):
        return sorted([player.player_no for player in self.wolves + self.villagers + [self.witch,self.seer,self.hunter] if player.alive])
    
    def player_out(self,player_no):
        for player in self.wolves + self.villagers + [self.witch,self.seer,self.hunter]:
            if player.player_no == player_no:
                player.alive = False
                break
        finished,result = self.finished()
        if finished:
            print(result)
            self.game_set()
            
    def finished(self):
        wolf_count = len([wolf for wolf in self.wolves if wolf.alive])
        villager_count = len([villager for villager in self.villagers if villager.alive])
        kami_count = int(self.witch.alive) + int(self.seer.alive) + int(self.hunter.alive)
        if wolf_count == 0:
            return True,"Villager win!"
        if kami_count == 0 or villager_count == 0:
            return True,"Wolf win!"
        return False,""
        
    def wolf_phase(self):
        print("----------Wolf Phase----------")
        vote_history = []
        player_vote_count = [0]*10
        for i in range(3):
            round_vote = []
            for wolf in self.wolves:
                if not wolf.alive:
                    continue
                voted = wolf.action(game_history=self.game_history,player_alive=self.get_alive_player_no(), vote_history=vote_history)
                print(f"Wolf Player {wolf.player_no} vote to kill Player {voted}")
                round_vote.append([wolf.player_no,int(voted)])
                player_vote_count[int(voted)] += 1
            vote_history.append(round_vote)
        max_count = max(player_vote_count)
        for i in range(1,10):
            tied = []
            print(f"Player {i} got {player_vote_count[i]} votes")
            if player_vote_count[i] == max_count:
                tied.append(i)
        if len(tied) == 1:
            print(f"Player {tied[0]} is killed by wolves")
            return tied[0]
        else:
            killed = random.choice(tied)
            print(f"Player {killed} is killed by wolves")
            return killed
        
                
    def night(self):
        print("==========Night==========")
        print("Wolves: ", self.wolves)
        print("Villagers: ", self.villagers)
        print("Witch: ", self.witch)
        print("Seer: ", self.seer)
        print("Hunter: ", self.hunter)
        player_out = []
        wolf_killed = self.wolf_phase()
        verified = self.seer.action(game_history=self.game_history,player_alive=self.get_alive_player_no())
        print(f"Seer verified Player {verified}")
        if self.witch.alive:
            save, poison = self.witch.action(game_history=self.game_history,player_alive=self.get_alive_player_no(),player_killed=wolf_killed,num_antidote=self.num_antidote,num_poison=self.num_poison)
            if len(self.game_history) == 0:
                if wolf_killed!=self.witch.player_no:
                    player_out.append(wolf_killed)
                else:
                    if save:
                        self.num_antidote = 0
            else:
                if save and self.num_antidote == 1:
                    self.num_antidote = 0
                    print("Witch saved Player",wolf_killed)
                elif wolf_killed == self.witch.player_no:
                    player_out.append(wolf_killed)
                elif poison!=0 and self.num_poison == 1:
                    self.num_poison = 0
                    player_out.append(poison)
                    print("Witch poisoned Player",poison)
                    player_out.append(wolf_killed)
                else:
                    player_out.append(wolf_killed)
        
        if self.hunter.alive and wolf_killed == self.hunter.player_no:
            shot = self.hunter.action(game_history=self.game_history,player_alive=self.get_alive_player_no())
            player_out.append(shot)
            print(f"Hunter shot Player {shot}")
        for player_no in player_out:
            self.player_out(player_no)
        print("=========Night End==========")
        return sorted(player_out)
                
    def speech(self, player_no, messages):
        for player in self.wolves + self.villagers + [self.witch,self.seer,self.hunter]:
            if player.alive and player.player_no == player_no:
                return player.speech(self.game_history,messages)
            
    def vote_phase(self,candidates):
        player_vote_count = [0]*10
        messages = []
        for player in self.wolves + self.villagers + [self.witch,self.seer,self.hunter]:
            if player.alive:
                vote = player.vote(self.game_history,[],candidates)
                print(f"Player {player.player_no} vote to kill Player {vote}")
                messages.append(f"Player {player.player_no} vote to kill Player {vote}")
                player_vote_count[int(vote)] += 1
        max_count = max(player_vote_count)
        sequence = []
        for i in range(1,10):
            if player_vote_count[i] == max_count:
                sequence.append(i)
        if len(sequence)==1:
            last_words = self.speech(sequence[0],messages+[f"Player {sequence[0]}, you have been sentenced as a werewolf, any last words?"])
            messages.append(f"Player {sequence[0]}'s last words: {last_words}")
            print(f"Player {sequence[0]}'s last words: {last_words}")
            self.player_out(sequence[0])
            print(f"Player {sequence[0]} is killed.")
            self.game_history.append("\n".join(messages))
            if sequence[0] == self.hunter.player_no:
                shot = self.hunter.action(game_history=self.game_history,player_alive=self.get_alive_player_no())
                print(f"Hunter shot Player {shot}")
                self.player_out(shot)
                print(f"Player {shot} is killed")
        else:
            player_vote_count = [0]*10
            for player_no in sequence:
                objection = self.speech(player_no,messages+[f"You have been sentenced as a werewolf, any objection?"])
                messages.append(f"Player {player_no}'s objection: {objection}")
                print(f"Player {player_no}'s objection: {objection}")
            for player in self.wolves + self.villagers + [self.witch,self.seer,self.hunter]:
                if player.alive:
                    frozen_messages = messages.copy()
                    vote = player.vote(self.game_history,frozen_messages,sequence)
                    print(f"Player {player.player_no} vote to kill Player {vote}")
                    messages.append(f"Player {player.player_no} vote to kill Player {vote}")
                    player_vote_count[int(vote)] += 1

            max_count = max(player_vote_count)
            sequence = []
            for i in range(1,10):
                if player_vote_count[i] == max_count:
                    sequence.append(i)
            if len(sequence)==1:
                last_words = self.speech(sequence[0],messages+[f"Player {sequence[0]}, you have been sentenced as a werewolf, any last words?"])
                messages.append(f"Player {sequence[0]}'s last words: {last_words}")
                print(f"Player {sequence[0]}'s last words: {last_words}")
                self.player_out(sequence[0])
                print(f"Player {sequence[0]} is killed.")
                self.game_history.append("\n".join(messages))
                if sequence[0] == self.hunter.player_no:
                    shot = self.hunter.action(game_history=self.game_history,player_alive=self.get_alive_player_no())
                    print(f"Hunter shot Player {shot}")
                    self.player_out(shot)
                    print(f"Player {shot} is killed.")
            else:
                messages.append("Tied, no one is killed.")
                self.game_history.append("\n".join(messages))

    def day(self, player_out):
        print("----------Day----------")
        player_out_message = f"Last night, Player {",".join(player_out)} was killed."
        print(player_out_message)
        alive_players = self.get_alive_player_no()
        print("Alive players: ", alive_players)
        if len(player_out) == 0:
            start = random.choice(alive_players)
        else:
            start = random.choice(player_out)
        print(f"Speech start from position {start}")
        messages = ["----------Day----------",player_out_message,f"Speech start from position {start}:"]
        upward = random.randint(0,1)
        if upward:
            for player_no in alive_players:
                if player_no >= start:
                    messages.append(f"Player {player_no}: {self.speech(player_no,messages)}")
                    print(f"Player {player_no}: {self.speech(player_no,messages)}")
            for player_no in alive_players:
                if player_no >= start:
                    break
                messages.append(f"Player {player_no}: {self.speech(player_no,messages)}")
                print(f"Player {player_no}: {self.speech(player_no,messages)}")
        else:
            for player_no in alive_players[::-1]:
                if player_no <= start:
                    messages.append(f"Player {player_no}: {self.speech(player_no,messages)}")
                    print(f"Player {player_no}: {self.speech(player_no,messages)}")
            for player_no in alive_players[::-1]:
                if player_no <= start:
                    break
                messages.append(f"Player {player_no}: {self.speech(player_no,messages)}")
                print(f"Player {player_no}: {self.speech(player_no,messages)}")

        self.game_history.append("\n".join(messages))
        self.vote_phase(alive_players)
        self.game_history.append("==========Night==========")
        print("----------Day End----------")
        
    def startgame(self):
        while True:
            player_out = self.night()
            self.day(player_out)