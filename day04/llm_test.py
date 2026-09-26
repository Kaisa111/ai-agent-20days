from openai import OpenAI
from dotenv import load_dotenv
import os


# 1. 加载 .env
load_dotenv()


# 2. 读取 API Key
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env")


# 3. 创建 OpenAI Client
client = OpenAI(api_key=api_key)


# 4. 调用 LLM
response = client.responses.create(
    model="gpt-5.6-luna",
    input="Explain Real-World Assets (RWA) in blockchain in one sentence."
)


# 5. 输出模型生成的文本
print("===== Answer =====")
print(response.output_text)

print("\n===== Model =====")
print(response.model)

print("\n===== Token Usage =====")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")