import vux

async def on_click(n: int):
    n += 1
    return {
        "n": n
    }

vux.page()(
    "# My Vux App",
    "Welcome to your first Vux app! [Docs](https://google.com)",
    vux.Button(
        "Click me! $n", 
        fn=on_click, 
        n=0
    )
)

vux.launch(host="0.0.0.0")
