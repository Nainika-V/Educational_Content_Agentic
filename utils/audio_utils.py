import edge_tts
import asyncio
import os
import time

AUDIO_FOLDER = "data/audio"

# create folder if not exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

async def generate_audio_async(text, file_path):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )
    await communicate.save(file_path)

def generate_audio(text):
    file_name = f"summary_{int(time.time())}.mp3"
    file_path = os.path.join(AUDIO_FOLDER, file_name)

    asyncio.run(generate_audio_async(text, file_path))

    return file_path