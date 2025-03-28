import httpx
import os
from openai import OpenAI, AzureOpenAI

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
FASTCHAT_BASE_URL = "http://127.0.0.1:5555/v1"  # 注意添加了/v1路径
prompt_token = 0
completion_token = 0

def get_total_usage():
    global prompt_token, completion_token
    return prompt_token, completion_token

# 初始化OpenAI客户端（用于云端API）
openai_client = OpenAI(
    base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else "https://api.openai.com/v1" ,
    api_key=OPENAI_API_KEY if OPENAI_API_KEY else "EMPTY",
    http_client=httpx.Client(
        base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else "https://api.openai.com/v1",
        follow_redirects=True,
    ),
)

# 初始化FastChat客户端（用于本地模型）
fastchat_client = OpenAI(
    base_url=FASTCHAT_BASE_URL,
    api_key="EMPTY",  # FastChat不需要验证的API密钥
)

def generate_response(messages, model="gpt-4o"):
    global prompt_token, completion_token

    if model.lower().startswith("llama"):
        # 使用FastChat客户端
        response = fastchat_client.chat.completions.create(
            model=model,  # 确保与FastChat注册的模型名称匹配
            messages=messages,
            temperature=0,
        )
    else:
        # 使用OpenAI客户端
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )

    # 统计Token使用量（兼容处理）
    try:
        prompt_token += response.usage.prompt_tokens
        completion_token += response.usage.completion_tokens
    except AttributeError:
        print("Warning: API响应中缺少usage信息，无法统计Token用量")

    return response.choices[0].message.content

if __name__ == "__main__":
    # 测试本地Llama模型
    messages = [
        {"role": "system", "content": "你是一个乐于助人的助手"},
        {"role": "user", "content": "美国的首都是哪里？"},
    ]
    
    # 测试OpenAI模型
    print("测试OpenAI模型:")
    print(generate_response(messages, "gpt-4o"))
    print(f"当前Token用量: {get_total_usage()}")
    
    # 测试FastChat本地模型
    print("\n测试本地Llama模型:")
    print(generate_response(messages, "llama-2-7b-chat"))  # 使用实际注册的模型名称
    print(f"当前Token用量: {get_total_usage()}")