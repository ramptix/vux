import uuid
from typing import Any, Callable, Dict, Union

from .base import Component, Flags, __loading__
from ..types import Action
from ..utils import clamp, create_repr, wrap_to_coro

OnClickAction = Callable[..., Union[str, Dict[str, Any]]]

class Button(Component):
    """Represents a button component.
    
    Args:
        label (str): The label.
        fn (OnClickAction): Function to execute when the button is clicked.
        **states (Any): States to pass to the ``fn``.
    """
    __has_actions__ = Flags.STARTUP_AND_EVENTS

    def __init__(
        self,
        label: str,
        fn: Union[OnClickAction, Action] = lambda: ...,
        **states: Any
    ):
        self.label_template = label
        self.states = states

        for state, value in self.states.items():
            if not state.startswith("_"):
                label = label.replace("$" + state, str(value))
        self.label = label
        self.raw_fn = fn
        self.fn = wrap_to_coro(fn)
        self.__id__ = str(uuid.uuid4())
        self.__html__ = (
            f"<button disabled data-control=\"{self.__id__}\">{__loading__}</button>".encode('utf-8')
        )

        listens = "{ listens: ['click'] }"
        self.__js__ = (
            f"""\
                $target.disabled = false;
                $target.textContent = "{label}";
                return {listens}
            """
        )

    async def on_event(self, event: str):
        if event == "click":
            kwargs = { k: v for k, v in self.states.items() if not k.startswith('_') }
            res = await self.fn(**kwargs)

            if isinstance(res, str):
                res = {
                    "$label": res,
                }
            
            elif isinstance(res, tuple):
                if len(res) != 2:
                    raise TypeError("Tuple should be size of 2: (str, dict)")
                
                pos = 0 if isinstance(res[0], str) else 1
                res = res[(pos + 1) % 2] | { "$label": res[pos] } # merge

            elif not isinstance(res, dict):
                raise TypeError(f"Unsupported type {type(event)} (return) for event handlers")
        
            if "$__dangerouslyExecuteJavascript" in res:
                del res['$__dangerouslyExecuteJavascript']

            label = res.get('$label', self.label_template)

            if "$label" in res:
                del res['$label']
            
            self.states.update(res)

            for state, value in self.states.items():
                if not state.startswith("_"):
                    label = label.replace("$" + state, str(value))

            return (
                f"""$target.textContent = {label!r};"""
            )

    def __repr__(self) -> str:
        return create_repr(
            name_nodes=["vux", "Button"],
            name_colors=["red", "blue"],
            label=clamp(self.label, ml=15),
            actions=True,
            startup=True
        )
