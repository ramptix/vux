import vux

async def click(num: int):
    num += 1
    raise KeyError("yo")
    return "Oopsy daisy!"

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

vux.launch(host="0.0.0.0") # launch the app