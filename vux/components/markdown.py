from markdown2 import Markdown as MarkdownParser

from .base import Component
from ..utils import clamp, create_repr


class Markdown(Component):
    """# `  M↓  `
    Represents a Markdown component.

    .. warning ::
        Don't trust/parse user-provided contents.

    Args:
        *text (str): The text.
    """
    __has_actions__ = None

    def __init__(
        self,
        *text: str
    ):
        parser = MarkdownParser()
        self.__html__ = parser.convert("\n\n".join(text)).encode('utf-8')
        self._original_text = " / ".join(text)

    def __repr__(self) -> str:
        return create_repr(
            name_nodes=["vux", "Markdown"],
            name_colors=["red", "blue"],
            text=clamp(self._original_text, ml=30)
        )
