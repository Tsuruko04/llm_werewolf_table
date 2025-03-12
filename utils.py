import httpx
import os
from openai import OpenAI
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    base_url=OPENAI_BASE_URL, 
    api_key=OPENAI_API_KEY,
    http_client=httpx.Client(
        base_url=OPENAI_BASE_URL,
        follow_redirects=True,
    ),
)
def generate_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of the United States?"},
    ]
    response = generate_response(messages)
    print(response)