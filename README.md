# Vux

Vux helps you create web apps backed by Python, hassle-free.

Get the Gradio feel, but faster.<sup>1</sup>

Key features:
- Simple syntax
- Fast
- Minimal dependencies<sup>2</sup>
- Async-ready

```haskell
$ pip install vux
```

<sub>1. Tested.</sub><br />
<sub>2. The Vux source code mostly uses low/medium API. For HTTP/WebSocket, Vux uses Uvicorn and not FastAPI because we want to keep the dependencies as clean as possible.</sub><br />

## Hello Vux.

A minimal example with Markdown and a simple form. Type hints compatible.

```python
import vux

async def hello_world(name: str, intensity: int = 1):
  return "Hello " * intensity + name

with vux.page() as page:
  page.add("# Vux Form")
  page.form(fn=hello_world)

vux.launch()
```

## Vux One

Vux One is a Vux branching project from Vux, designed specifically for browsers (clients). No server computation needed.

```js
import one from '@ramptix/vux1'
```
