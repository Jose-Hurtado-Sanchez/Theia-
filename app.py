# FastAPI server wrapper for fall detection.
# Has REST endpoints for simulatingf falls, sensor data, and canelling fall alerts. 


from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
import asyncio
import threading
import time

from fall_detector import FallDetector, FallConfig

app = FastAPI(title="Theia Fall Detection Service", version="1.0")

# Allows cross origin requests from local dev frontends (Flutter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory demo storage
# demo contacts
CONTACTS: List[Dict[str, str]] = [
    {"label": "Caretaker", "phone": "+1-555-123-4567"},
]

# Settings 
SETTINGS = FallConfig()

# Placeholder, UI/navigation can post current building, floor, room
CONTEXT: Dict[str, Any] = {
    "building": None,
    "floor": None,
    "room": None,
    "destination": None,
}

# queue for events, simple fanout to websocket clients using direct sends
event_queue: "asyncio.Queue[Dict[str, Any]]" = asyncio.Queue()
# Track connected websocket clients 
_ws_clients: "set[WebSocket]" = set()

# add context to event payloads
def _enrich_with_context(evt: Dict[str, Any]) -> Dict[str, Any]:
    return {**evt, "context": CONTEXT.copy()}

# Push event to queue and broadcast to connected websockets
async def _push_event(evt: Dict[str, Any]):
    evt = _enrich_with_context(evt)
    # enqueue for polling clients
    await event_queue.put(evt)
    # broadcast to websocket clients 
    dead: List[WebSocket] = []
    for ws in list(_ws_clients):
        try:
            await ws.send_json(evt)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _ws_clients.discard(ws)

# Detector callbacks
def _on_detect(evt_obj, countdown_s):
    coro = _push_event({"type": "fall.detected", "countdown": countdown_s, "peak_g": round(evt_obj.peak_g, 2)})
    asyncio.get_event_loop().call_soon_threadsafe(asyncio.create_task, coro)

def _on_cancel():
    coro = _push_event({"type": "fall.canceled"})
    asyncio.get_event_loop().call_soon_threadsafe(asyncio.create_task, coro)

def _on_escalate():
    coro = _push_event({"type": "fall.escalated", "contacts": CONTACTS, "message": "Possible fall detected"})
    asyncio.get_event_loop().call_soon_threadsafe(asyncio.create_task, coro)

# Create detector instance
detector = FallDetector(SETTINGS, _on_detect, _on_cancel, _on_escalate)

# Background ticker thread to drive countdown expiration
def _ticker_loop():
    while True:
        detector.tick()   # checks for countdown expiration and triggers escalate via callback
        time.sleep(0.1)   # 100ms tick

_thread = threading.Thread(target=_ticker_loop, daemon=True)
_thread.start()

# models for REST inputs
class Accel(BaseModel):
    ax: float
    ay: float
    az: float

class ContactIn(BaseModel):
    label: str
    phone: str

class SettingsIn(BaseModel):
    impact_g: float | None = None
    inactivity_g: float | None = None
    inactivity_window_s: float | None = None
    debounce_s: float | None = None
    countdown_s: int | None = None

class ContextIn(BaseModel):
    building: str | None = None
    floor: int | None = None
    room: str | None = None
    destination: str | None = None


# REST Endpoints

@app.get("/status")
def status():
    return {
        "ok": True,
        "settings": SETTINGS.__dict__,
        "contacts_count": len(CONTACTS),
        "context": CONTEXT,
    }

@app.get("/contacts")
def get_contacts():
    return CONTACTS

@app.post("/contacts")
def add_contact(c: ContactIn):
    CONTACTS.append(c.model_dump())
    return {"ok": True, "contacts": CONTACTS}

@app.delete("/contacts/{idx}")
def delete_contact(idx: int):
    if 0 <= idx < len(CONTACTS):
        CONTACTS.pop(idx)
        return {"ok": True, "contacts": CONTACTS}
    raise HTTPException(status_code=404, detail="Contact index out of range")

@app.get("/settings")
def get_settings():
    return SETTINGS.__dict__

@app.post("/settings")
def set_settings(s: SettingsIn):
    # updates provided fields
    provided = s.model_dump(exclude_none=True)
    for k, v in provided.items():
        if hasattr(SETTINGS, k):
            setattr(SETTINGS, k, v)
    return {"ok": True, "settings": SETTINGS.__dict__}

@app.post("/context")
def set_context(ctx: ContextIn):
    provided = ctx.model_dump(exclude_none=True)
    for k, v in provided.items():
        CONTEXT[k] = v
    return {"ok": True, "context": CONTEXT}

@app.post("/sensor/accel")
def post_accel(a: Accel):
    # input sample to detector
    detector.feed_accel(a.ax, a.ay, a.az)
    return {"ok": True}

@app.post("/fall/simulate")
def simulate_fall():
    # demo endpoint to run simulated impact sequence
    detector.simulate_fall()
    return {"ok": True}

@app.post("/fall/cancel")
def cancel_fall():
    detector.cancel()
    return {"ok": True}

@app.get("/events")
async def poll_events():
    
    # simple polling endpoint, returns and clears all queued events currently in the queue, clients can poll periodically if they cannot use WebSockets.
  
    items: List[Dict[str, Any]] = []
    try:
        while True:
            items.append(event_queue.get_nowait())
    except asyncio.QueueEmpty:
        pass
    return items

# WebSocket endpoint for realtime events
@app.websocket("/ws")
async def websocket_events(ws: WebSocket):
    
    # Clients can open a websocket connection here and will receive events when they happen.
    
    await ws.accept()
    _ws_clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        _ws_clients.discard(ws)
