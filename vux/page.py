from __future__ import annotations

from copy import deepcopy
from typing import Any, List, Literal, Optional, Union

from .cache import CACHE
from .components import Component, component_lookup
from .components.base import Flags
from .utils import clamp, is_notebook

ContentType = Union[Literal["markdown"], Component]

class page:
    """Represents a Vux page.

    Example:
        .. code-block :: python3

            import vux
            with vux.page() as page:
                page.add("# Hello Vux!")
    
    Args:
        id (str): Page ID. Defaults to ``home``.
    """
    components: List[Component]
    page_title: Optional[str]
    page_id: str

    def __init__(self, id: str = "home"):
        if id in CACHE.pages:
            if not is_notebook():
                raise NameError(
                    f"Page id {clamp(id)!r} is already in use."
                )

        self.page_id = id
        self.components = []
        self.page_title = None

    def add(
        self,
        *contents: Any,
        type: ContentType = "markdown",
        **kwargs: Any
    ):
        """Adds a component to the current page. (*method*)

        You can also use ``page()`` if you want to type less.

        Example:
            .. code-block :: python3

                with vux.page() as page:
                    page.add(
                        "# I love Markdown!",
                        "If you prefer markdown, raise your hand!"
                    )

        Args:
            *contents (Any): The contents.
            type (ContentType): The component type.
            **kwargs (Any): Extra configs to send to the component class.
        """
        return self.__call__(*contents, type=type, **kwargs)

    def title(self, __title: str):
        """Assign the page title.
        
        Args:
            __title (str): The title.
        """
        self.page_title = __title
        self.update()

        return self

    def __call__(
        self, 
        *contents: Any, 
        type: ContentType = "markdown",
        **kwargs: Any
    ):
        """Adds a component to the current page. (*method*)

        You can also use ``page.add()`` if you prefer a clearer syntax.

        Example:
            .. code-block :: python3

                with vux.page() as page:
                    page(
                        "# I love Markdown!",
                        "If you prefer markdown, raise your hand!"
                    )

        Args:
            *contents (Any): The contents.
            type (ContentType): The component type (as default).
            **kwargs (Any): Extra configs to send to the component class (as default).
        """
        comp = component_lookup.get(type) or type

        for content in contents:
            self.components.append(
                comp(content, **kwargs)
                if not issubclass(content.__class__, Component)
                else content
            )

        self.update()

        return self

    def _prepare(self):
        self.mapping = {
            c.__id__: c
            for c in self.components
            if c.__has_actions__
        }

    def __enter__(self) -> page:
        return self
    
    def __exit__(self, *_):
        self.update()

    def update(self):
        CACHE.pages[self.page_id] = self

    def copy(self):
        return deepcopy(self)

    @property
    def __html__(self) -> bytes:
        return b"\n".join([c.__html__ for c in self.components])

    @property
    def __startup__(self) -> dict:
        return {
            c.__id__: c.__js__
            for c in self.components
            if c.__has_actions__ in (Flags.ONLY_STARTUP, Flags.STARTUP_AND_EVENTS)
        }
