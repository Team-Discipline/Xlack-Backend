from typing import Union

from fastapi import Cookie, Depends, APIRouter, Query, WebSocket, status
from fastapi.responses import HTMLResponse

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


@router.get("/")
async def get_feature():
    return HTMLResponse(html)


@router.websocket('/websocket')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        chats = await websocket.receive_text()
        await websocket.send_text(f"Message: {chats}")


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Union[str, None] = Cookie(default=None),
        token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


