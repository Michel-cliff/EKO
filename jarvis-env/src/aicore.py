import time
from config import MISTRAL_API_KEY
from mistralai import Mistral

client = Mistral(api_key=MISTRAL_API_KEY)

def ask_mistral(prompt):
    """Send conversation history to Mistral for multi-turn context."""
    response = None
    for attempt in range(5):
        try:
            response = client.chat.complete(
                model="mistral-small",
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except Exception as e:
            print(f"Error: {e} (attempt {attempt+1})")
            time.sleep(2 ** attempt)

    if response is None:
        return "Sorry, I couldn't get a response from Mistral."

    return response.choices[0].message.content
