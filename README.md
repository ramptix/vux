# Vux

Welcome to Vux!

Vux helps you create beautiful Python-based web apps without additional configurations and provides a clean API for developers.
You can use Vux to create Markdown documentation or build a demo for your ML (machine-learning) models like [Gradio](https://gradio.app). 

But seriously, we aren't that good enough.

Key features:
- Simple: quick starts need to be fast!
- Async-ready: supported by [Uvicorn](https://uvicorn.org)
- WebSocket: stay connected, my friend
- Flexible: very bendable
- Fast: ⚡⚡

```haskell
$ pip install vux
```

## 🪴 Getting Started

To get started, try out our "Hello Vux" code below and learn from examples.

```python
import vux

async def click(num: int):
    num += 1
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

<br />

Vux also provides a Form API so you can create a demo of an ML model more efficiently. Just add some type hints, and Vux will automatically determine the input & output types!

```python
import vux

async def form(
  name: str,
  intensity: int = 1
) -> str:
  return "Hello " * intensity + name

with vux.page() as page:
  page.add(
    vux.Form(fn=form)
  )
```

If you prefer the [Gradio](https://gradio.app) syntax, the `vux.Form` component also supports `inputs` and `outputs=` arguments.

## 🤓 Some Words

**Naming**

> The name "Vux" doesn't really mean anything in English nor in other languages. I looked up some weird names of Apple MacOS and discovered the version "Ventura." Since everybody loves the letter "X" as much as our lizard boy's opponent Elon Musk, let's take the "V" and "u" from the word "Ventura," and add an additional "X" as the decoration.
>
> ("Vu" is just way too similar to "Vue" and is literally a reference to Deja Vu.)

**API Concepts**

> I really love FastAPI's concept in one word—`typing`. Nothing too special: it's human readable and easy to understand. Additionally, I referred to the `useState()`  API from React, and thought it'd be cool if we can also do that for Python web apps.
> 
> So I did. Cool.

***

(c) 2024 Ramptix
