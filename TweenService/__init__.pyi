"""This module acts similarly to Roblox's TweenService API with extended classes and options."""

from typing import TypedDict, Callable, NotRequired, Self, Any, overload
from collections import deque
from threading import Thread

class TweenInfo_T(TypedDict):
    time: NotRequired[int | float]
    style: NotRequired[str]
    delay: NotRequired[int | float]
    repeat_count: NotRequired[int]
    reverses: NotRequired[bool]

class TweenInfo:
    """Stores the TweenInfo for tweening process. \n \n
    To serialize TweenInfo, the name of the function must in the globals. \n
    Use 'from TweenService.Easings import *' or 'from TweenService.Easings import <required EasingFunctions>'
    if you are using the built-in Easing Styles and serialize TweenInfo. \n
    Defaults:
    - time: 1
    - style: TweenService.Easings.Linear
    - delay: 0
    - repeat_count: 0
    - reverses: False"""

    @overload
    def __init__(self, time: int | float = 1, style: Callable[[int | float], float] | None = None, 
                 delay: int | float = 0, repeat_count: int = 0, reverses: bool = False) -> None:
        self.time: int | float
        self.style: Callable[[int | float], float] # what im i gonna do with this treated as literal function
        self.delay: int | float 
        self.repeat_count: int
        self.reverses: bool

    @overload
    def __init__(self, _dict: TweenInfo_T): ...
    
    def to_dict(self) -> TweenInfo_T: 
        """Returns a dictionary version of TweenInfo."""
        ...

    def from_dict(self) -> Self:
        """Converts dictionary to TweenInfo.""" 
        ...

class TweenHandler:
    def __init__(self, object: object, tweenInfo: TweenInfo_T | TweenInfo, target: dict[str, Any], 
                 thread = None) -> None:
        self.target_object: Any
        self.tweenInfo: TweenInfo_T
        self.target_property: dict[str, Any]
        self.thread: TweenThread

    def start(self) -> Self: 
        """Starts the tween."""
        ...

    def update(self) -> bool:
        """Update wrapper for updating values of tween. Returns bool for tween success"""
        ...

class TweenThread:
    """A thread to run tweening updates."""
    def __init__(self, cycles = 60) -> None:
        self.thread: Thread
        self.cycles: int
        self.stopped: bool
        self.items: deque[TweenHandler]

    def get_items(self) -> deque[TweenHandler]: ...
    def add_item(self, tw: TweenHandler) -> None: ...
    def update(self) -> None: ...
    def stop(self) -> Self: ...
    def start(self) -> Self: ...

    @staticmethod
    def __update_wrap__(self_obj): ...

GlobalTweenThread: TweenThread | None