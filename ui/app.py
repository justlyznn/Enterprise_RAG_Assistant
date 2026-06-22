import chainlit as cl
from api.rag_pipeline import get_rag_pipeline

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Halo! Saya adalah Intelligent Customer Assistant 🤖. Tanyakan sesuatu mengenai layanan kami!",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        # Panggil pipeline langsung (lebih cepat dan aman untuk Single-Container)
        pipeline = get_rag_pipeline()
        answer = await cl.make_async(pipeline.answer_question)(message.content)
    except Exception as e:
        answer = f"Terjadi kesalahan sistem: {e}"

    await cl.Message(content=answer).send()
