from typing import Dict

from .base import Component
from .button import Button
from .markdown import Markdown

component_lookup: Dict[str, Component] = {
    "markdown": Markdown,
    "button": Button
}
