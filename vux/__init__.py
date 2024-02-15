"""# Vux (beta)

Vux provides a clean interface for all kinds of Python web applications.

Its API is clean and newcomers friendly.

To get started, use the ``vux.page`` context manager and create your first page.

.. code-block :: python3

    >>> import vux
    >>> # use context manager
    >>> with vux.page() as page:
    ...    page("Hello, **markdown**!")
    >>> # launch the app
    >>> vux.launch()

For more information, visit https://github.com/ramptix/vux
"""

from .components import Button, Markdown
from .launch import launch
from .page import page

__all__ = [
    'Button',
    'Markdown',
    'launch',
    'page',
]
