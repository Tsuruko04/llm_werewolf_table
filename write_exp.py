from utils import generate_response
with open("./experience/qwen7b.txt","r") as f:
    qwen = f.read()
    prompt = """
    You are a game master of the game Werewolves.
    Here's a few experiences of playing the game Werewolves:{experiences}
    """
    result = generate_response([{'role':'system','content':prompt.format(experiences=qwen)},{'role':'user','content':"Please give a summary of the game strategies based on the experiences."}],model="qwen2.5-7b-instruct")
    
with open("./strategy/qwen2.5-7b-instruact.txt","w") as f:
    f.write(result)
    print(result)