from abc import ABC, abstractclassmethod as abcmethod
from enum import Enum
from typing import Optional


class Flags(Enum):
    ONLY_STARTUP = 1 << 0
    ONLY_EVENTS = 1 << 1
    STARTUP_AND_EVENTS = 1 << 2

class Component(ABC):
    """Represents a base component. (*abc*)
    
    Not initializable by default.
    """
    __slots__ = (
        "__html__",
    )
    __html__: bytes
    __has_actions__: Optional[Flags] = False
    __js__: Optional[str] = None
    __id__: Optional[str] = None

    @abcmethod
    def __repr__(self) -> str:
        ...

__loading__ = (
    """\
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" 
        viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" 
        fill="none" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="vux-loader-svg"    
    >
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <path d="M12 6l0 -3"></path>
        <path d="M16.25 7.75l2.15 -2.15"></path>
        <path d="M18 12l3 0"></path>
        <path d="M16.25 16.25l2.15 2.15"></path>
        <path d="M12 18l0 3"></path>
        <path d="M7.75 16.25l-2.15 2.15"></path>
        <path d="M6 12l-3 0"></path>
        <path d="M7.75 7.75l-2.15 -2.15"></path>
    </svg>
    """
).strip()
