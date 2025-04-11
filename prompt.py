game_rules = """
We follow the 9-player standard mode Werewolf game rules. The rules are outlined as follows.

1. Objectives
The game is divided into two factions: the "Good" faction, which includes Villagers and special roles, and the "Werewolf"
faction. Additionally, there is a Moderator who is responsible for managing the game and ensuring the rules are followed.
The goal for the "Good" faction is to identify and execute all Werewolves, while the goal for Werewolves is to kill or exile
all Villagers or all special roles. The game ends when any of the following conditions are met:
• All Villagers are out of the game (Werewolves win)
• All special roles are out of the game (Werewolves win)
• All Werewolves are out of the game ("Good" faction win)

2. Roles
The game comprises 3 Villagers, 3 Werewolves, and 3 special roles (Seer, Witch, and Hunter). The identities of the players
are hidden from each other, even after being eliminated from the game.
Werewolves: Werewolves are aware of each other’s identities. At night, they decide to kill a living player, which can include
themselves. The majority of the Werewolves’ choice will be the final kill target. If there is a tie, a random player in the
tie is killed. Werewolves can commit suicide during the speech sessions, which will reveal their identity, and the game
immediately proceeds to the night phase, skipping the remaining daytime processes such as speeches and voting.
Villagers: Villagers have no special abilities. They must determine other players’ identities based on their speeches and vote
to exile potential Werewolves.
Seer: The Seer can verify a player’s faction each night (a Werewolf or the "Good"), but cannot know their specific role. The
Seer cannot verify himself or any player who has already been verified.
Witch: The Witch possesses an antidote and a poison. The antidote can save a player killed by Werewolves at night, and the
poison can kill a player. The Witch cannot use both potions in the same night and can only save herself on the first night.
Hunter: When the Hunter is killed by Werewolves at night or voted out during the day, he can shoot a player. However, the
Hunter cannot use his ability when poisoned by the Witch.

3. Game Task Flow

The game proceeds in a night-day cycle until the victory conditions are met.
The night tasks flow:
(1) Werewolves decide to kill a player. In our simulation of the game environment, we have simplified the discussion into a
three-round voting process. During voting, werewolf players can see their teammates’ previous votes.
(2) The Witch uses her ability.
(3) The Seer uses his ability.
The daytime tasks flow:
(1) The Moderator announces the deaths from last night but does not reveal the causes of death.
(2) Deceased players give their last words (only for the first day).
(3) If deceased players have additional abilities, they may choose to use them.
(4) First round of speeches. The speech sequence is determined by the following rules: (a) if no player died last night,
randomly select an initial speaker and randomly decide a clockwise or counterclockwise speaking order. (b) randomly
select a deceased player and start the speaking order clockwise or counterclockwise from him. Players cannot interrupt
others during their speeches.
(5) First round of voting. Each player votes for a single player to exile from the game. Other players’ voting choices
remain hidden until the voting session ends.
(6) Second round of speeches. If there is a tie in the first round of voting, the tied players give their second speeches;
otherwise, the process moves on to task (8) The first speaker, selected randomly from the tied players, initiates the
sequence, which could proceed either clockwise or counterclockwise.
(7) Second round of voting. If there is still a tie after the second vote, the game moves on to the next night, and no player is
exiled.
(8) The exiled player gives his last words.
(9) If exiled players have additional abilities, they may choose to use them.
"""

wolfgame_background ="""
# Task Scenario: 9-player Werewolf game speech.
"Good" Faction:
- 3 Villagers
- 1 Seer
- 1 Witch
- 1 Hunter
Werewolf Faction:
- 3 Werewolves
Common terminologies are explained as follows:
1. Werewolf, bandit, wolf, bad faction, knife: Werewolf.
2. Villager, civilian, white card: Villager.
3. Seer, prophet: Seer.
4. Witch, witch card: Witch.
5. Hunter, gun: Hunter.
6. Gold, gold water, verified Good: A good person verified by the Seer.
7. Verify Kill: A Werewolf verified by the Seer.
8. Silver, silver water, Werewolves’ target, Saved: A person saved by the Witch.
9. Iron, steel, certain: Very certain, e.g., "Player 3 is an iron Werewolf"
or "Player 3 is definitely the Werewolf," indicates that Player 3 is certainly a
Werewolf.
10. Jump: A player declares his/her role (not necessarily his/her true role).
11. Backstab: A Werewolf sides with the good people, betraying their own
teammates.
12. Defame: To demean the identity of other players.
13. Exalt: To believe in the identity of other players.
14. Vote out, point, nominate, ballot: Voting, e.g., "Vote for Player 6 or Player
7," means to vote Player 6 or Player 7 out.
"""

speech_understanding_requirements = """
# Task requirements are as follows:
Based on your understanding of the game state and speeches, please output the
extraction results in JSON format in sequence. The format should be:
{
"identities": {"<identity>": [player,player,...]} ,
"actions": {"<action>": [subject player -> object player,
subject player -> object player]}
}
Example:
{
"identities": {"werewolf":[3,5]}, "seer":[1], "gold water":[6]}
"actions": {"check":[1->6, 2->3]}
}
- This indicates Players 3 and 5 are werewolves, Player 1 checks Player 6, and Player
2 checks Player 3.
- Player numbers can only be: 1, 2, 3, 4, 5, 6, 7, 8, 9.
- When players express their intentions, please correspond to the identity of the
player, for example, if Player 5 speaks, then consider from the perspective of
Player 5.
- The subject number should be inferred from the context, such as ’I’, ’you’, ’he’,
’she’, etc. If unknown, use ’unknown’, for example: "check":[unknown->6].

Possible JSON KEYs are:
Identities:
- Roles: Seer, Witch, Hunter, Villager, Werewolf, "Good" faction, Werewolf faction,
gold water, silver water, the werewolves’ target, etc.
- Guess: suspicious, credible, uncertain, tolerant, etc.
- Speech: good (up), bad (down), listen well, listen to kill, etc.
- Faction: allied, support, werewolf candidate, etc.
- Online status: disconnected, offline, not online, voice, etc.
Actions:
- Skills:
    - Seer: check, inspect.
    - Witch: poison, save.
    - Hunter: shoot, take away, crash, kill.
    - Werewolf: self-destruct, explode.
- And skills that will be used in the future:
    - Vote: vote out, choose a target, etc.
- Quotes from other Players’ statements do not need to be summarized.
- Note the distinction between quantifiers and player numbers: must be, that there
are three werewolves.
- Note negative statements: not, impossible, implausible, not quite, etc.
- Note the abbreviation of number + information, e.g., "three golds, nine slashes,
one, six, eight, three wolves" results in:"identities": "gold water":[3],
"slash":[9], "werewolf":[1,6,8]
"""
speech_examples_few_shot = """
# The following are examples of speeches:

"I checked Player 6, and I suggest Player 8 turn around and vote
for Player 6. I will check the identity of Player 4 in the next round."

"Player 2 and I are collaboratively searching for a Seer. Player
2 assists the good faction in combating werewolves. There’s a possibility that
Player 9 is a werewolf, although I am not certain. The behavior of Player 9 seems
suspiciously similar to that of Player 2, who possesses the ability to shoot.
Additionally, Player 4 is identified as a Witch. Regarding the usage of silver
water, I suggest targeting Player 6."

"Player 8 is the gold water. Player 2 is not a werewolf, neither
is Player 3. However, Player 7 is suspicious, and I recommend voting against Player
7. The roles of Player 4 and Player 5 are unclear, and Player 1 suspects both of
them to be werewolves. I advise Player 7 to use poison, which could help confirm
my role as a Seer. Concerning the hunter, there is a standoff between Player 8
and myself. If there is any uncertainty about Players 1, 2, or 4, the gun should
be used in this situation against Player 2. Now, it’s time for Players 4 and 7 to
present their arguments, and there is no need to focus on Player 9."

"Being the first player to speak, my turn was conveniently arranged.
However, I am uncertain about Player 2’s allegiance. In my view, Player 2 lacks
credibility."

"Player 3 will be poisoned tonight. I hold the Witch card. I heed
the guidance of the two players with gold cards. Players 9 and 5 are identified as
wolves. Players 4 and 6 hold cards corresponding to their numbers, with Player 4
being more trustworthy than Player 5. Player 3 cannot be revived. To preserve my
own safety, I will reveal myself as the Witch. I have already used the silver water
card on Player 1. Player 9 remarked that I should be pleased with this misfortune,
indicating that the prime werewolf card was passed to a fellow teammate."

"Player 5 appears highly suspicious. He could either be a werewolf
or might be deceiving his teammates. His failure to set wolf traps, dishonesty
about the wheat sequence, and excessive talking during the first microphone turn is
concerning. Players 6 and 7 might be superficial wolves. Player 7, however, seems
to have a sensible perspective and could be part of the good camp. I recommend
voting against Player 5."

"Regarding the game, my suspicion falls on Players 1, 5, 7, and 
3 as potential wolves. The accusation by Player 3, however, is incorrect. I find
Player 3’s judgment flawed. It’s frustrating. Similarly, I suspect that Players 1,
5, 7, and 3 are wolves according to Player 5’s perspective. Let’s test this theory.
I propose we eliminate Player 5 today, and then I, as a Witch, will poison Player 7
tomorrow night. Observe the game’s progression tomorrow, and you will see that both
Player 5 and I, as Witches, agree on Player 2, and our views align with Player 3’s
decision. Therefore, I request that we focus on Player 5 first."

"""
information_extraction_few_shot = """
# The following are 11 speeches and corresponding information extraction examples:
Player 3 spoke: "I checked Player 6, and I suggest Player 8 turn around and vote
for Player 6. I will check the identity of Player 4 in the next round."
{
"identities":{"seer":[3],"werewolf":[1,6,8]},
"actions":{"check":[3->6],"suggest to vote":[8->6],
"check in the next round":[3->4]}
}
Player 7 spoke: "Player 2 and I are collaboratively searching for a Seer. Player
2 assists the good faction in combating werewolves. There’s a possibility that
Player 9 is a werewolf, although I am not certain. The behavior of Player 9 seems
suspiciously similar to that of Player 2, who possesses the ability to shoot.
Additionally, Player 4 is identified as a Witch. Regarding the usage of silver
water, I suggest targeting Player 6."
{
"identities":{"maybe a wolf":[9],"hunter":[2],"silver water":[4]},
"actions":{"suggest to vote":[7->6]}
}
Player 9 spoke: "Player 8 is the gold water. Player 2 is not a werewolf, neither
is Player 3. However, Player 7 is suspicious, and I recommend voting against Player
7. The roles of Player 4 and Player 5 are unclear, and Player 1 suspects both of
them to be werewolves. I advise Player 7 to use poison, which could help confirm
my role as a Seer. Concerning the hunter, there is a standoff between Player 8
and myself. If there is any uncertainty about Players 1, 2, or 4, the gun should
be used in this situation against Player 2. Now, it’s time for Players 4 and 7 to
present their arguments, and there is no need to focus on Player 9."
{
"identities":{"gold water":[8],"good camp":[2,3],"suspicious":[7],
"werewolf":[4,5],"seer":[9] ,"werewolf candidate":[1,2,4],
"hunter":[2],"debate players":[4,7]},
"actions":{"suggest to vote":[9->7],"suggest to poison":[unknown->7]}
}
Player 3 spoke: "Being the first player to speak, my turn was conveniently arranged.
However, I am uncertain about Player 2’s allegiance. In my view, Player 2 lacks
credibility."
{
"identities":{"no result": []},
"actions":{"no result": []}
}
Player 7 spoke: "Player 3 will be poisoned tonight. I hold the Witch card. I heed
the guidance of the two players with gold cards. Players 9 and 5 are identified as
wolves. Players 4 and 6 hold cards corresponding to their numbers, with Player 4
being more trustworthy than Player 5. Player 3 cannot be revived. To preserve my
own safety, I will reveal myself as the Witch. I have already used the silver water
card on Player 1. Player 9 remarked that I should be pleased with this misfortune,
indicating that the prime werewolf card was passed to a fellow teammate."
{
"identities":{"witch":[7],"gold water":[2],"werewolf":[9,5],"suspicious":[4]},
"actions":{"suggest to poison":[7->3],"believe to be a silver water":[7->1]}
}
Player 8 spoke: "Player 5 appears highly suspicious. He could either be a werewolf
or might be deceiving his teammates. His failure to set wolf traps, dishonesty
about the wheat sequence, and excessive talking during the first microphone turn is
concerning. Players 6 and 7 might be superficial wolves. Player 7, however, seems
to have a sensible perspective and could be part of the good camp. I recommend
voting against Player 5."
{
"identities":{"suspicious":[5],"werewolf":[6,7],"good camp":[7]},
"actions":{"suggest to vote":[8->5]}
}
Player 2 spoke: "Regarding the game, my suspicion falls on Players 1, 5, 7, and
3 as potential wolves. The accusation by Player 3, however, is incorrect. I find
Player 3’s judgment flawed. It’s frustrating. Similarly, I suspect that Players 1,
5, 7, and 3 are wolves according to Player 5’s perspective. Let’s test this theory.
I propose we eliminate Player 5 today, and then I, as a Witch, will poison Player 7
tomorrow night. Observe the game’s progression tomorrow, and you will see that both
Player 5 and I, as Witches, agree on Player 2, and our views align with Player 3’s
decision. Therefore, I request that we focus on Player 5 first."
{
"identities":{"werewolves’ target":[3],"werewolf":[1,5,7],"witch":[2]},
"actions":{"suggest to vote":[2->5, 2->7]}
}
Player 1 spoke: "Player 6 is engaging in killing actions. Players 5 and 7 have
been poisoned. Players 4 and 5 are both targeting Player 1. Player 3 has been
stabbed, and it’s possible that Players 2, 4, and 9 each represent a threat, akin
to three knives. Player 5 has revealed themselves as the Witch and has provided
Player 3 with a dose of silver water."
{
"identities":{"seer":[1],"poison":[5,7],"depreciate":[4,5],
"werewolves’ target":[3],"werewolf":[2, 4,9],"witch":[5]},
"actions":{"check":[1->6],"believe to be a silver water":[5->3]}
}
Player 1 spoke: "I, Player 1, am part of the good faction. The focus of today’s
game is on Players 3 and 5. Player 9 might be a werewolf. I did not use any poison
last night."
{
"identities":{"good camp":[1],"werewolf":[9]},
"actions":{"suggest to vote":[1->3,1->5]}
}
Player 9 spoke: "I am the Hunter. Player 7 has self-destructed. Player 2 might
be associated with the silver water. As for myself, I reiterate that I am the
Hunter. Player 1 is acting suspiciously, resembling a white card. I request the
Witch to acknowledge this. Player 3 is overly concerned with external cards, which
is uncharacteristic of a Prophet. Players 3 and 8, please return to the game, as
there’s still an opportunity for a round of confrontation."
{
"identities":{"hunter":[9],"self-destruction":[7],"silver water and seer":[2],
"white":[1],"not like a seer":[3] },
"actions":{"suggest to vote":[9->3,9->8]}
}
Player 4 spoke: "I believe Player 6 is trustworthy as he revealed Player 6’s key
card. My intention is to verify Player 3. Player 7, who holds the gold water,
should cast their vote against Player 8. It’s evident that Players 3 and 7 are not
the same individual. On the field, there are only two players acting as villagers.
I have identified the three wolves. There is no necessity to doubt Player 7;
instead, Player 4 can be acknowledged as the Seer."
{
"identities":{"gold water":[7],"seer":[4]},
"actions":{"consider credible":[4->6],"verified":[4->3],
"suggest to vote":[4->8]}
}
"""

villager_prompt = """
You are a player in a 9-player Werewolf game.
{game_rules}
Your identity is assigned as a Villager.
You are Player {player_no}.
"""

werewolf_prompt = """
You are a player in a 9-player Werewolf game.
{game_rules}
Your identity is assigned as a Werewolf.
You are Player {player_no}. The werewolves on the table are Player {wolves_no}.
"""

werewolf_action_prompt = """
Now, you need to decide on your action for the night. You can choose to kill a player.
The majority of the Werewolves’ choice will be the final kill target. If there is a tie, a random player in the tie is killed.
Here's the voting history:
{voting_history}
End of the history:
Please provide the player number you choose to kill. Players remained: {players}. Your teammates are: {wolves_no}. Please only provide the number. As a werewolf, I choose to kill:
"""

witch_prompt = """
You are a player in a 9-player Werewolf game.
{game_rules}
Your identity is assigned as a Witch.
You are Player {player_no}.
"""

witch_action_prompt = """
Now, you need to decide on your action for the night. You can choose to save a player or poison a player.
The Witch cannot use both potions in the same night and can only save herself on the first night.
Player {player_killed} has been killed by the Werewolves at night, you have {num_antidote} antidote.
If you want to use your poison, please provide a player number. You have {num_poison} poison.
If you don't want to use your poison, please choose number 0.
Remeber, you can only use either antidote or poison in a night.
Answer whether you want to save the player killed by Werewolves or which player you want to poison.
Only choose from the players remained: {players}.
As the witch, I think:
"""

seer_prompt = """
You are a player in a 9-player Werewolf game.
{game_rules}
Your identity is assigned as a Seer.
You are Player {player_no}.
"""

seer_action_prompt = """
Now, you need to decide on your action for the night. You can choose a player to verify whether him/her is a werewolf.
Please provide a player number. Players remained: {players}. Only provide the number. As the seer, I choose to check:
"""

hunter_prompt = """
You are a player in a 9-player Werewolf game.
{game_rules}
Your identity is assigned as a Hunter.
You are Player {player_no}.
"""

hunter_action_prompt = """
You have been out, now you can choose a player to shoot.
Please provide a player number. Players remained: {players}. If you don't want to shoot, please provide 0. Only provide the number. 
I choose to shoot:
"""

vote_prompt = """
Now, it's your turn to vote a player to be sentenced. Please provide a player number from the following players: {players}. If you don't want to vote, please provide 0. Only provide the number.
As player {player_no}, I choose to vote:
"""

parse_wolf_action_prompt = """
The werewolf gives the following response: {response}
Please parse the response and provide the player number that the werewolf has decided to kill.
Only provide the number. For example: Given "I choose to kill Player 4.", you should respond with 4
"""

parse_witch_action_prompt = """
The witch gives the following response: {response}
The antidote can save a player killed by Werewolves at night, and the poison can kill a player.
Please parse the response and give your answer in the format: [yes|no],<player_no>. For example, if the witch want to save player 8 with antidote, please answer: yes,0; if neither want to save nor poison, answer: no,0; if poison player 3, answer: no,3.
""" 
parse_seer_action_prompt = """
The seer gives the following response: {response}
Please parse the response and provide the player number that the seer has decided to check.
Only provide the number. For example: Given "I choose to check Player 4.", you should respond with 4
"""
parse_hunter_action_prompt = """
The hunter gives the following response: {response}
Please parse the response and provide the player number that the hunter has decided to kill.
Only provide the number. For example: Given "I choose to kill Player 4.", you should respond with 4
"""

parse_vote_prompt = """
The player gives the following response: {response}
Please parse the response and provide the player number that the player has decided to vote.
Only provide the number. For example: Given "I choose to vote Player 4.", you should respond with 4. If no player mentioned or you can't decide, please respond 0.
"""

summarize_game_experience_prompt = """
Now the game is over. As the {role} in this game, please analyze the reason for your victory or defeat.
Give your own experience of being a {role} in this game. I think:
"""