import asyncio
import base64
import hashlib
import inspect
import os
import re
from typing import Callable, Dict, List, Literal, Tuple

from .types import Action, RawHeaders


esc_RESET = "\033[0m"
HERE = os.path.dirname(__file__)
STATIC = os.path.join(HERE, "./static")

def hex_to_rgb(hex: str) -> Tuple[int, int, int]:
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def gen_color_esc(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def colored(hex: str) -> str:
    rgb = hex_to_rgb(hex)
    return gen_color_esc(*rgb)

def create_repr(
    name_nodes: List[str],
    name_colors: List[Literal["red", "gray", "orange", "green"]],
    **kwargs
):
    assert len(name_nodes) == len(name_colors)


    C = colored
    c_map = {
        "red": "#e06c75",
        "gray": "#abb2bf",
        "orange": "#d19a66",
        "green": "#98c379",
        "blue": "#56b6c2"
    }
    repr_name = ""

    for i, nn in enumerate(name_nodes):
        repr_name += C(c_map[name_colors[i]]) + nn + esc_RESET

        if i < len(name_nodes) - 1:
            repr_name += C(c_map['gray']) + '.' + esc_RESET

    attrs = " "

    for i, (key, name) in enumerate(kwargs.items()):
        attrs += (
            C(c_map['orange']) + key + esc_RESET +
            C(c_map['gray']) + '=' + esc_RESET +
            C(c_map['green']) + f'{name!r}' + esc_RESET
        ) + " "

    return f"{C(c_map['gray'])}<{repr_name}{attrs}{C(c_map['gray'])}/>{esc_RESET}"

def clamp(t: str, *, ml: int = 20):
    """Clamp.
    
    Args:
        t (str): Text.
        ml (int): Max length. Defaults to ``20``.
    """
    return (t[:ml + 1] + "…") if len(t) > ml else t

def template(html: bytes, **kwargs) -> str:
    shtml = html.decode('utf-8')

    for k, v in kwargs.items():
        shtml = shtml.replace(
            "{% " + k + " %}", 
            v.decode('utf-8') if isinstance(v, bytes) else str(v)
        )

    return shtml.encode('utf-8')

def wrap_to_coro(fn: Action) -> Callable:
    if inspect.iscoroutinefunction(fn):
        return fn
    
    async def wrapper(*args, **kwargs):
        # run_in_executor does not support **kwargs
        def runner():
            return fn(*args, **kwargs)

        return await asyncio.get_event_loop().run_in_executor(None, runner)
    
    return wrapper

def get_websocket_accept_key(client_key: bytes) -> bytes:
    magic = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    concat = client_key + magic
    sha1_hash = hashlib.sha1(concat).digest()
    key = base64.b64encode(sha1_hash)

    return key

def headers_to_dict(headers: RawHeaders) -> Dict[bytes, bytes]:
    return {
        k.lower(): v for k, v in headers
    }

def format_exc(exc: str):
    replacements = re.findall(r'(File ".+"), line \d+, in .*', exc)

    for repl in replacements:
        
        exc = exc.replace(repl, repl.replace("\\", "\\\\"))
    
    return exc

def is_notebook():
    # https://stackoverflow.com/questions/15411967
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:
            return False
        
    except ImportError:
        return False
    
    except AttributeError:
        return False
    
    return True