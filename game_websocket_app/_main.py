from fastapi import FastAPI, Response
from pydantic import BaseModel
from starlette.websockets import WebSocket
from starlette.middleware.cors import CORSMiddleware 

app = FastAPI()

# 接続中のクライアントを識別するためのIDを格納
key2name = {}
key2ws = {}
rooms = []

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class Room(BaseModel):
    name: str

@app.get("/")
def get_index():
    return Response(content=data, media_type="text/html")

@app.get("/rooms")
def get_rooms():
    return {"rooms": rooms}

@app.get("/rooms")
def get_rooms():
    return {"rooms": rooms}

# WebSockets用のエンドポイント
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    key2ws[key] = ws
    try:
        while True:
            # クライアントからメッセージを受信
            data = await ws.receive_text()
            # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
            for client in key2ws.values():
                await client.send_text(f"ID: {key} | Message: {data}")
    except:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]
