import gc
import os
import traceback
from typing import List, Optional

import uvicorn

from .cache import CACHE
from .utils import STATIC, format_exc, template
from .websocket import WebSocket

with open(os.path.join(STATIC, "index.html"), "rb") as f:
    HTML = f.read()

with open(os.path.join(STATIC, "index.js"), "rb") as f:
    JAVASCRIPT = f.read()

with open(os.path.join(STATIC, "app.css"), "rb") as f:
    CSS = f.read()

async def respond(send, *, headers: List[List[bytes]], status: int, body: bytes):
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers
    })
    await send({
        'type': 'http.response.body',
        'body': body
    })

async def uvicorn_app(scope, receive, send):
    if scope['type'] == 'http':
        if scope['path'] in ("/index.js", "/app.css"):
            ext = scope['path'].split('.')[-1]
            return await respond(
                send,
                headers=[
                    [b'content-type', b'text/javascript' if ext == 'js' else b'text/css']
                ],
                status=200,
                body=JAVASCRIPT if ext == 'js' else CSS
            )

        await respond(
            send,
            headers=[
                [b'content-type', b'text/html']
            ],
            status=200,
            body=template(
                HTML, 
                title=CACHE.pages['home'].page_title or "Vux App",
                root=CACHE.pages['home'].__html__
            )
        )
    
    elif scope['type'] == 'websocket':
        ws = WebSocket(scope, receive, send)
        await ws.accept()

        page = CACHE.pages['home'].copy()
        await ws.send_json({
            "t": "startup",
            "d": page.__startup__
        })

        try:
            while True:
                payload = await ws.receive_json()

                if payload['t'] == 'update':
                    # {"t": "update", "d": {"id": "...", "event": "click" }}
                    component_id = payload['d']['id']
                    d = await page.mapping[component_id].on_event(payload['d']['event'])

                    await ws.send_json({
                        "t": "update",
                        "d": {
                            component_id: d
                        }
                    })

                elif payload['t'] == 'heartbeat':
                    await ws.send_json({ "t": "heartbeat" })

        except ConnectionAbortedError:
            return

        except Exception as error:
            exc = format_exc(traceback.format_exc())
            summarization = exc.splitlines()[-1]

            await ws.send_json({
                "t": "error",
                "d": {
                    "err": exc,
                    "sum": summarization
                }
            })
            await ws.close()
            raise error # raise it again
        
        finally:
            del page
            gc.collect()
        

def launch(*, host: Optional[str] = None, port: int = 5000, **kwargs):
    """Launch your app.
    
    Vux finds the nearest pages available.
    """
    if not CACHE.pages:
        raise ValueError(
            "No pages configured"
        )

    CACHE.pages['home']._prepare()

    config = uvicorn.Config(uvicorn_app, host=host or "172.0.0.1", port=port, **kwargs)
    server = uvicorn.Server(config)

    server.run()
