# For reference, the following code is from 
# @encode/starlette on GitHub
# Huge shoutout for helping me to implement WebSocket 
# connections with only Uvicorn.

import json
from typing import Callable, Optional

from .types import RawHeaders

PENDING = 0
CONNECTED = 1
DISCONNECTED = 2

class WebSocket:
    """Represents a websocket."""

    def __init__(
        self,
        scope: dict,
        receive: Callable[[], dict],
        send: Callable[[dict], None]
    ):
        self._scope = scope
        self._recv = receive
        self._send = send
        self._state = PENDING

    async def accept(
        self,
        *, 
        subprotocol: Optional[str] = None,
        headers: Optional[RawHeaders] = None
    ):
        if self._state == PENDING:
            # If we haven't seen the 'connect' message, then wait for it first.
            assert (await self._recv())['type'] == 'websocket.connect'

        if self._state == DISCONNECTED:
            raise ConnectionRefusedError("Disconnected")

        await self._send({
            'type': 'websocket.accept',
            'subprotocol': subprotocol,
            'headers': headers or []
        })
        self._state = CONNECTED

    async def send_json(
        self,
        message: dict
    ):
        if self._state == PENDING:
            raise ConnectionError("state is PENDING (0), must accept() first.")
    
        await self._send({
            'type': "websocket.send",
            'text': json.dumps(message)
        })

    async def receive(self) -> str:
        d = await self._recv()

        if self._state != CONNECTED:
            raise ConnectionRefusedError("Not connected (1)")

        if d['type'] == 'websocket.disconnect':
            raise ConnectionAbortedError("WebSocket disconnected")
        
        elif d['type'] == 'websocket.receive':
            return d['text']
        
        else:
            raise RuntimeError(d['type'])
        
    async def receive_json(self):
        return json.loads(await self.receive())
    
    async def close(self):
        await self._send({
            'type': 'websocket.close',
            'reason': 'server_runtime_error'
        })
        self._state = DISCONNECTED
