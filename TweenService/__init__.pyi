"""This module acts similarly to Roblox's TweenService API with extended classes and options."""

from typing import TypedDict, Callable, NotRequired, Self, Any, overload, Literal
from collections import deque
from threading import Thread

DEFAULT_TWEEN_TIME: Literal[1]
DEFAULT_TWEEN_STYLE: Callable[[int | float], int | float]
DEFAULT_TWEEN_DELAY: Literal[0]
DEFAULT_TWEEN_REPEAT_COUNT: Literal[0]
DEFAULT_TWEEN_REVERSES: Literal[False]

TWEEN_EVENT_TYPE_DEFAULT: Literal[0]
TWEEN_EVENT_TYPE_ONCE: Literal[1]

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

    def get(self, key: str) -> Any: ...

class TweenEvent:
    def __init__(self, name: str):
        self.events: deque[tuple[Callable[..., Any], int]]
        self.name: str
    def Connect(self, func: Callable[..., Any], append_left: bool = False): ...
    def Disconnect(self, func: Callable[..., Any]): ...
    def Once(self, func: Callable[..., Any], append_left: bool = False): ...
    def Fire(self, *args, **kwargs): ...

class TweenHandler:
    def __init__(self, object: object, tweenInfo: TweenInfo_T | TweenInfo, target: dict[str, Any], 
                 thread = None) -> None:
        self.target_object: Any
        self.tweenInfo: TweenInfo_T
        self.target_property: dict[str, Any]
        self.thread: TweenThread

        self.Completed: TweenEvent
        self.TweenStarted: TweenEvent
        self.StartCalled: TweenEvent

        self.start_time: int | float

    def GetTweenInfo(self) -> TweenInfo: ...
    def GetTweenInfoData(self, key) -> Any: ...

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

def init(cycles: int = 60) -> TweenThread: ...
def create_main_thread(cycles: int = 60) -> TweenThread: ...