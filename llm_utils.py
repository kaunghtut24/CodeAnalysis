import os
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_code_with_llm(code: str, prompt: Optional[str] = None) -> str:
    if not prompt:
        prompt = (
            "You are a code analysis assistant. Analyze the following Python code for quality, bugs, and improvements. "
            "Provide a concise summary and suggestions."
        )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": code}
        ],
        max_tokens=512,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
