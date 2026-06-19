import chainlit as cl
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Halo! Saya adalah Intelligent Customer Assistant 🤖. Tanyakan sesuatu mengenai layanan kami!",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    # Prepare request to FastAPI
    try:
        # We use a synchronous request here but run it in a thread if needed,
        # but for simplicity requests.post is fine for this demo.
        response = requests.post(
            f"{API_URL}/chat", 
            json={"query": message.content}, 
            timeout=120
        )
        if response.status_code == 200:
            answer = response.json().get("response", "Maaf, tidak ada respons dari server.")
        else:
            answer = f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        answer = f"Gagal terhubung ke API: {e}"

    # Send response back to the user
    await cl.Message(content=answer).send()
