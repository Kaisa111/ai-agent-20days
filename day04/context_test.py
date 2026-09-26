from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


response1 = client.responses.create(
    model="gpt-5.6-luna",
    instructions="""
    You are a crypto research assistant.
    Answer clearly and concisely.
    """,
    input="My favorite crypto asset is Bitcoin."
)

print("===== Round 1 =====")
print(response1.output_text)


response2 = client.responses.create(
    model="gpt-5.6-luna",
    previous_response_id=response1.id,
    input="What is my favorite crypto asset?"
)

print("\n===== Round 2 =====")
print(response2.output_text)