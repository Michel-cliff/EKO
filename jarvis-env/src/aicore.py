import time
from config import MISTRAL_API_KEY
from mistralai import Mistral

client = Mistral(api_key=MISTRAL_API_KEY)

def ask_mistral(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.chat.complete(
                model="mistral-small",
                messages=[{"role": "user", "content": "Hello Jarvis!"}]
            )
            break
        except Exception as e:
            print(f"Error: {e} (attempt {attempt+1})")
            time.sleep(2 ** attempt)  # exponential backoff
    return response.choices[0].message.content