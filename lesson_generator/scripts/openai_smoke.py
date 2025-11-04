import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except Exception as e:
    print("ERROR: openai import failed:", e)
    raise

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY is not set")
    raise SystemExit(2)

client = OpenAI(api_key=api_key)

try:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a test."},
            {"role": "user", "content": "Reply with just: OK"},
        ],
        temperature=0,
        max_tokens=2,
    )
    print("COMPLETION:", (resp.choices[0].message.content or "").strip())
except Exception as e:
    print("ERROR: openai call failed:", type(e).__name__, str(e))
    raise
