from enum import Enum
from utils import generate_response
import prompt 
import yaml
PARSE_MODEL = yaml.safe_load(open("./settings.yaml", "r"))["parse_model"]
print("PARSE_MODEL:",PARSE_MODEL)
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
        self.model = None
        self.strategy = None
    def __repr__(self):
        return f"Player {self.player_no}({self.model})(Alive: {self.alive})"
    
    def __str__(self):
        return f"Player {self.player_no}({self.model})(Alive: {self.alive})"
    
    def action(self,game_history,player_alive, **kwargsargs):
        if self.role == Role.WEREWOLF:
            return self.wolf_action(game_history,player_alive,kwargsargs["vote_history"])
        if self.role == Role.WITCH:
            return self.witch_action(game_history,player_alive,kwargsargs["player_killed"],kwargsargs["num_antidote"],kwargsargs["num_poison"])
        if self.role == Role.SEER:
            return self.seer_action(game_history,player_alive,kwargsargs["black_sheep_wall"])
        if self.role == Role.HUNTER:
            return self.hunter_action(game_history,player_alive)
        
    def role_prompt(self):
        if self.role == Role.WEREWOLF:
            return prompt.werewolf_prompt.format(game_rules=prompt.game_rules+prompt.wolfgame_background,player_no = self.player_no,wolves_no=self.private_message)
        if self.role == Role.VILLAGER:
            return prompt.villager_prompt.format(game_rules=prompt.game_rules+prompt.wolfgame_background,player_no = self.player_no)
        if self.role == Role.WITCH:
            return prompt.witch_prompt.format(game_rules=prompt.game_rules+prompt.wolfgame_background,player_no = self.player_no)
        if self.role == Role.SEER:
            return prompt.seer_prompt.format(game_rules=prompt.game_rules+prompt.wolfgame_background,player_no = self.player_no)
        if self.role == Role.HUNTER:
            return prompt.hunter_prompt.format(game_rules=prompt.game_rules+prompt.wolfgame_background,player_no = self.player_no)
        return ""
    
    def strategy_prompt(self):
        if self.strategy:
            return f"""
            Here's some strategies of playing the game Werewolves:
            {self.strategy}
            """
        else:
            return ""
    def wolf_action(self, game_history, player_alive,vote_history):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)
        act_prompt = self.strategy_prompt()+prompt.werewolf_action_prompt.format(voting_history="\n".join(vote_history),players = player_alive, wolves_no = self.private_message)
        return self._parse_wolf_action(generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt},{'role':'user','content':act_prompt}],model=self.model))
    
    def witch_action(self, game_history, player_alive,player_killed,num_antidote,num_poison):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)
        act_prompt = self.strategy_prompt()+prompt.witch_action_prompt.format(player_killed = player_killed,num_antidote=num_antidote,num_poison=num_poison,players = player_alive)
        result = generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt},{'role':'user','content':act_prompt}],model=self.model)
        return self._parse_witch_action(result)
        
    def seer_action(self,game_history,player_alive,black_sheep_wall):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)+f"As the Seer, you have known that: "+ "\n".join(self.private_message)
        act_prompt = self.strategy_prompt()+prompt.seer_action_prompt.format(players = player_alive)
        verified = self._parse_seer_action(generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt},{'role':'user','content':act_prompt}],model=self.model))
        self.private_message.append(f"Player {verified} is {black_sheep_wall[verified]}")
        return verified
    
    def hunter_action(self,game_history,player_alive):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)
        act_prompt = self.strategy_prompt()+prompt.hunter_action_prompt.format(players = player_alive)
        return self._parse_hunter_action(generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt},{'role':'user','content':act_prompt}],model=self.model))
    
    def speech(self,game_history,messages):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)
        if self.role==Role.SEER:
            private_info = "As a seer, you have known that: "+ "\n".join(self.private_message)
        elif self.role==Role.WITCH:
            private_info = "As a witch, you have known that: "+ "\n".join(self.private_message)
        else:
            private_info = ""
        speech_prompt = self.strategy_prompt()+"The discussion and voting of the current phase are:\n" + "\n".join(messages)+ "\nNow, it's your turn to speak. Rememebr, you are actually playing the game, every word you reply will be known by other players. Please only provide the speech content. Your response should be short and concise. Please provide who you think is the werewolf and why in the speech."
        return generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt+private_info+speech_prompt}],model=self.model)

    
    def vote(self,game_history,messages,candidates):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)
        private_info = "As a seer, you have known that: "+ "\n".join(self.private_message) if self.role==Role.SEER else ""
        messages_prompt = self.strategy_prompt()+"The discussion and voting of the current phase are:\n" + "\n".join(messages)
        vote_prompt = prompt.vote_prompt.format(players = candidates, player_no = self.player_no)
        return self._parse_vote(generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt+private_info},{'role':'user','content':messages_prompt+vote_prompt}],model=self.model))

    def _parse_wolf_action(self, text):
        print("THOUGHT:",text)
        return int(generate_response([{'role':'system','content':prompt.wolfgame_background},{'role':'user','content':prompt.parse_wolf_action_prompt.format(response=text)}],model=PARSE_MODEL))
        
    def _parse_witch_action(self, text):
        print("THOUGHT:",text)
        while True:
            try:
                result =  generate_response([{'role':'system','content':prompt.wolfgame_background},{'role':'user','content':prompt.parse_witch_action_prompt.format(response=text)}],model=PARSE_MODEL)
                save,poison = result.split(',')
                if save in ["yes","Yes","YES"]:
                    save = True
                    poison = 0
                else:
                    save = False
                    poison = int(poison)
                return save, poison
            except:
                pass
            
    def _parse_seer_action(self, text):
        print("THOUGHT:",text)
        try:
            return int(text)
        except:
            return int(generate_response([{'role':'system','content':prompt.wolfgame_background},{'role':'user','content':prompt.parse_seer_action_prompt.format(response=text)}],model=PARSE_MODEL))
    
    def _parse_hunter_action(self, text):
        print("THOUGHT:",text)
        try:
            return int(text)
        except:
            return int(generate_response([{'role':'system','content':prompt.wolfgame_background},{'role':'user','content':prompt.parse_hunter_action_prompt.format(response=text)}],model=PARSE_MODEL))
    
    def _parse_vote(self, text):
        print("THOUGHT:",text)
        try:
            return int(text)
        except:
            return int(generate_response([{'role':'system','content':prompt.wolfgame_background},{'role':'user','content':prompt.parse_vote_prompt.format(response=text)}],model=PARSE_MODEL))
    
    def summarize_game_experience(self, game_history):
        role_prompt = self.role_prompt()
        game_prompt = "The public history information of the ongoing game is:\n" + "\n".join(game_history)
        
        act_prompt = prompt.summarize_game_experience_prompt.format(role=self.role.name)
        
        return generate_response([{'role':'system','content':role_prompt+"\n"+game_prompt},{'role':'user','content':act_prompt}],model=self.model)
if __name__ == "__main__":
    player = Player(1)
    player.role = Role.WEREWOLF
    player.model="qwen2.5-7b-instruct"
    player.private_message = [1,2,3]
    # print(player.action([],[i for i in range(1,10)],vote_history=[]))
    print(player.summarize_game_experience([]))
