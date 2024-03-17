import uuid

from .components import Component, Markdown
from .components.base import Flags
from .page import page


class _StaticMarkdownRoot(Component):
    def __init__(self, t: str):
        self.__id__ = str(uuid.uuid4())
        self.__html__ = f"<p data-control=\"{self.__id__}\"></p>".encode('utf-8')
        self.__has_actions__ = Flags.ONLY_STARTUP
        self.__js__ = (
            f"""$target.removeAttribute('data-control');
            $target.textContent = {t!r}"""
        )

    def __repr__(self) -> str:
        return "(root-static)"

class static(page):
    """Represents a static page.
    
    Once sent to the client side, it will be cached and cannot 
    perform any client-server actions.

    Usually it's a static Markdown/plain text page.
    """
    def __init__(self, *text: str, id: str = "home", plain: bool = False):
        super().__init__(id=id)
        self.add(Markdown(*text) if not plain else _StaticMarkdownRoot("\n\n".join(text)))

