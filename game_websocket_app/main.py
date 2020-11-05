from typing import List, Dict, Tuple
from pydantic import BaseModel

from fastapi import FastAPI, WebSocket, Form
from fastapi.responses import HTMLResponse
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


INDEX_FILE = "/app/tmp.html"
CHAT_FILE = "/app/chat.html"
with open(INDEX_FILE) as f:
    index_html = f.read()

with open(CHAT_FILE) as f:
    chat_room_html = f.read()

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class User(BaseModel):
    name: str
    room_id: int


class ConnectionManager:
    def __init__(self):
        self.rooms: List[str] = ["alpha", "beta"]
        self.active_connections: List[List[WebSocket]] = [[],[]]
        self.members: List[List[str]] = [[],[]]

    def create_room(self, room_name: str):
        self.rooms.append(room_name)
        self.active_connections.append([])
        self.members.append([])

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


@app.get("/")
async def get():
    return HTMLResponse(index_html)


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


@app.post("/chat")
async def enter_room(room_id: int = Form(...), user_name: str = Form(...)):
    return HTMLResponse(chat_room_html % (user_name, manager.rooms[room_id], room_id, user_name))


@app.websocket("/ws/{room_id}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_name: str):
    await manager.connect(websocket, room_id, user_name)
    await manager.broadcast(room_id, f"Client #{user_name} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(room_id, f"Client #{user_name} says: {message}")
    except:
        manager.disconnect(websocket, room_id, user_name)
        await manager.broadcast(room_id, f"Client #{user_name} left the chat")
