from typing import List, Dict, Tuple
from pydantic import BaseModel
import time

from fastapi import FastAPI, WebSocket, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware 

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


DIR = "/app/dist/"
INDEX_FILE = DIR + "index.html"
TALKS_FILE = DIR + "talks.html"

with open(INDEX_FILE) as f:
    index_html = f.read()

with open(TALKS_FILE) as f:
    talks_html = f.read()

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class User(BaseModel):
    name: str
    room_id: int


class ConnectionManager:
    def __init__(self):
        self.rooms: List[str] = ["alpha", "beta"]
        self.active_connections: List[List[WebSocket]] = [[] for i in range(len(self.rooms))]
        self.members: List[List[str]] = [[] for i in range(len(self.rooms))]
        self.hees = [0 for i in range(len(self.rooms))]

    def create_room(self, room_name: str):
        self.rooms.append(room_name)
        self.active_connections.append([])
        self.members.append([])
        self.hees.append(0)

    async def connect(self, websocket: WebSocket, room_id: int, user_name: str):
        await websocket.accept()
        self.active_connections[room_id].append(websocket)
        self.members[room_id].append(user_name)

    def disconnect(self, websocket: WebSocket, room_id: int, user_name: str):
        self.active_connections[room_id].remove(websocket)
        self.members[room_id].remove(user_name)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, room_id: int, message: str):
        for connection in self.active_connections[room_id]:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/rooms")
async def get_rooms():
    return {"rooms": manager.rooms}


@app.post("/rooms/{room_name}")
async def create_room(room_name: str):
    manager.create_room(room_name)
    return {"room_id": len(manager.rooms) - 1}


@app.get("/{room_id}/members")
async def get_rooms(room_id: int):
    return {"members": manager.members[room_id]}


@app.post("/talks")
async def enter_room(room_id: int = Form(...), user_name: str = Form(...)):
    return HTMLResponse(talks_html % (user_name, manager.rooms[room_id], room_id, user_name))


@app.websocket("/ws/{room_id}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_name: str):
    await manager.connect(websocket, room_id, user_name)
    await manager.broadcast(room_id, f"TXT:{user_name} joined the chat")
    await manager.broadcast(room_id, f"HEE:{manager.hees[room_id]}")
    await manager.send_personal_message(f"TXT:Welcome to {manager.rooms[room_id]}", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            head = data[:4]
            body = data[4:]
            if head == "TXT:":
                await manager.send_personal_message(f"{head}You wrote: {body}", websocket)
                message = f"{head}{user_name} says: {body}"
            elif head == "HEE:":
                manager.hees[room_id] += 1
                message = f"{head}{manager.hees[room_id]}"
            await manager.broadcast(room_id, message)
    except:
        manager.disconnect(websocket, room_id, user_name)
        await manager.broadcast(room_id, f"TXT:{user_name} left the chat")
