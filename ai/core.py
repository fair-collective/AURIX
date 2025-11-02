# aurix/ai/core.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests, json

app = FastAPI(title="AURIX AI Kernel")

class Command(BaseModel):
    text: str
    user: str = "founder"

@app.post("/speak")
async def speak(cmd: Command):
    # Call Grok API or local LLM
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": "Bearer YOUR_GROK_KEY"},
        json={
            "model": "grok-beta",
            "messages": [{"role": "user", "content": cmd.text}],
            "stream": False
        }
    ).json()
    text = response["choices"][0]["message"]["content"]
    
    # ElevenLabs TTS
    tts = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
        headers={"xi-api-key": "YOUR_ELEVEN_KEY"},
        json={"text": text, "voice_settings": {"stability": 0.9}}
    )
    return tts.content, {"Content-Type": "audio/mpeg"}
