import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

# 1. Force load .env
load_dotenv()

async def check():
    print("--- Diagnostic Start ---")
    
    # 2. Check Key
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        print("[ERROR] OPENROUTER_API_KEY is missing from environment.")
        return
    
    masked = key[:8] + "..." + key[-4:]
    print(f"[INFO] API Key loaded: {masked}")
    print(f"[INFO] Base URL: {os.getenv('OPENROUTER_BASE_URL')}")

    # 3. Test Connection
    client = AsyncOpenAI(
        api_key=key,
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    )

    print("[INFO] Attempting to connect to OpenRouter...")
    print(f"[INFO] Using model: {os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-v3')}")
    try:
        completion = await client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v3"),
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=10
        )
        print("[SUCCESS] Connection established!")
        print(f"[RESPONSE] {completion.choices[0].message.content}")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check())
