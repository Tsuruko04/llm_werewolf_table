import httpx
import os
from openai import OpenAI,AzureOpenAI
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(
#     base_url=OPENAI_BASE_URL, 
#     api_key=OPENAI_API_KEY,
#     http_client=httpx.Client(
#         base_url=OPENAI_BASE_URL,
#         follow_redirects=True,
#     ),
# )
client = AzureOpenAI(
    api_key = OPENAI_API_KEY,
    azure_endpoint= OPENAI_BASE_URL,
    api_version= "2024-05-01-preview"
)
def generate_response(messages):
    response = client.chat.completions.create(
        model="gpt-4-1106",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of the United States?"},
    ]
    response = generate_response(messages)
    print(response)