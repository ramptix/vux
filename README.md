# Vux

Welcome to Vux!

Vux helps you create beautiful Python-based web apps without additional configurations and provides a clean API for developers.
You can use Vux to create Markdown documentation or build a demo for your ML (machine-learning) models like [Gradio](https://gradio.app). 

But seriously, we aren't that good enough.

Key features:
- Simple: quick starts need to be fast!
- Async-ready: supported by [Uvicorn](https://uvicorn.org)
- Flexible: very bendable
- Fast: ⚡⚡

```haskell
$ pip install vux
```

## Getting Started

To get started, try out our "Hello Vux" code below and learn from examples.

```python
import vux

async def click(num: int):
    return { "num": num }

# create a home page
with vux.page() as page:
    page.add(
        "# Hello Vux",
        vux.Button(
            label="Click me! $num",
            fn=click,
            num=0
        )
    )

vux.launch() # launch the app
```

The Vux syntax is flexible, so there are many ways to write a single page. Pick the one that's most suitable for your projects and use it thoroughly so that you can maintain them more easily. (Be nice to your [coworkers](https://www.youtube.com/watch?v=6BMOk7zvKEE).)
