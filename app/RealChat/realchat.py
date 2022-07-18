from typing import Union, List

from fastapi import Cookie, Depends, APIRouter, Query, WebSocket, status, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.model.schemas import Chat

router = APIRouter(prefix='/features/real_chat', tags=['RealChat'])

# TODO: html file required(please put UI here)
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
</html>
"""


class ConnectionCheck:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_chat(self, chat: str, websocket: WebSocket):
        await websocket.send_text(chat)

    async def broadcast(self, chat: str):
        for connection in self.active_connections:
            await connection.send_text(chat)


check = ConnectionCheck()


@router.get("/")
async def get_feature():
    return HTMLResponse(html)


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Union[str, None] = Cookie(default=None),
        token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket('/items')
async def websocket_endpoint(websocket: WebSocket, chatter=Chat.chatter_name,
                             query: Union[int, None] = None, cookie: str = Depends(get_cookie_or_token)):
    await websocket.accept()
    try:
        while True:
            chat_db = await websocket.receive_text()
            await websocket.send_text(f"Session cookie : {cookie}")
            await check.send_personal_chat(f"You:{chat_db}", websocket)
            await check.broadcast(f"from client {chatter} chat: {chat_db}")
            if query is not None:
                await websocket.send_text(f"Query parameter query: {query}")
    except WebSocketDisconnect:
        check.disconnect(websocket)
        await check.broadcast(f"chatter {chatter} left this chat")
