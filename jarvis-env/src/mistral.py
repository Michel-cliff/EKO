import os
import time
from mistralai import Mistral

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

for attempt in range(5):
    try:
        response = client.chat.complete(
            model="mistral-small",
            messages=[{"role": "user", "content": "Hello Jarvis!"}]
        )
        print(response.choices[0].message.content)
        break
    except Exception as e:
        print(f"Error: {e} (attempt {attempt+1})")
        time.sleep(2 ** attempt)  # exponential backoff