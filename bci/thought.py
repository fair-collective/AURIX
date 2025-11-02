# aurix/bci/thought.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import json

active_brains: Dict[str, WebSocket] = {}

@app.websocket("/bci")
async def bci_stream(websocket: WebSocket):
    await websocket.accept()
    brain_id = websocket.headers.get("x-brain-id", "unknown")
    active_brains[brain_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            intent = json.loads(data)
            # Example: {"intent": "open", "target": "aurora"}
            await route_thought(intent, brain_id)
    except WebSocketDisconnect:
        del active_brains[brain_id]

async def route_thought(intent: dict, brain_id: str):
    action = f"Thought from {brain_id}: {intent['intent']} {intent.get('target', '')}"
    print(action)
    # Trigger AI, open app, deploy code
    await broadcast_to_holo(action)
