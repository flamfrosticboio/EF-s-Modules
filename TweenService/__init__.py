from typing import TypedDict, NotRequired, overload
from collections import deque
from time import time as get_time, sleep
from threading import Thread
from TweenService.Easings import Linear

def _print_warning(type, message):
    print("\033[93m" + type + ": " + message + "\033[0m")

DEFAULT_TWEEN_TIME = 1
DEFAULT_TWEEN_STYLE = Linear
DEFAULT_TWEEN_DELAY = 0
DEFAULT_TWEEN_REPEAT_COUNT = 0
DEFAULT_TWEEN_REVERSES = False

TWEEN_EVENT_TYPE_DEFAULT = 0
TWEEN_EVENT_TYPE_ONCE = 1

class TweenInfo_T(TypedDict):
    time: NotRequired[int | float]
    style: NotRequired[str]
    delay: NotRequired[int | float]
    repeat_count: NotRequired[int]
    reverses: NotRequired[bool]

class TweenInfo:
    def __init__(self, time = 1, style = None, delay = 0, repeat_count = 0, reverses = False):
        if isinstance(time, dict):  # overloading the worse way possible
            self.time = time.get("time", DEFAULT_TWEEN_TIME)
            self.style = time.get("style", DEFAULT_TWEEN_STYLE)
            self.delay = time.get("delay", DEFAULT_TWEEN_DELAY)
            self.repeat_count = time.get("repeat_count", DEFAULT_TWEEN_REPEAT_COUNT)
            self.reverses = time.get("reverses", DEFAULT_TWEEN_REVERSES)
        else:
            self.time = time
            self.style = style if style else Linear
            self.delay = delay
            self.repeat_count = repeat_count
            self.reverses = reverses

    def __repr__(self) -> str:
        kwargs = [f'{n}={m}' for n, m in self.__dict__.items()]
        kwargs[1] = f"style={self.style.__name__}"   # simple fix to serialize style name
        return f"{self.__class__.__name__}({', '.join(kwargs)})"
    
    def to_dict(self):
        return dict(self.__dict__.items())
    
    def get(self, key):
        return self.__dict__.get(key)

GlobalTweenThread = None

class TweenEvent:
    def __init__(self, name):
        self.events = deque()
        self.name = name

    def _wrap_func(self, func, type = TWEEN_EVENT_TYPE_DEFAULT):
        return (func, type)

    def Connect(self, func, append_left = False):
        func = self._wrap_func(func)
        if append_left == True:
            self.events.appendleft(func)
        else:
            self.events.append(func)

    def Disconnect(self, func):
        for _func, _t in self.events.copy():
            if _func == func: self.events.remove((_func, _t)); return
        _print_warning(f"[TweenEvent:{self.name}] Warning: Cannot find function {func} to Disconnect.")
    
    def Once(self, func, append_left = False):
        func = self._wrap_func(func, TWEEN_EVENT_TYPE_ONCE)
        if append_left == True:
            self.events.appendleft(func)
        else:
            self.events.append(func)

    def Fire(self, *args, **kwargs):
        for _func, _t in self.events.copy():
            _func(*args, **kwargs)
            if _t == TWEEN_EVENT_TYPE_ONCE:
                self.events.remove((_func, _t)) 

class TweenHandler:
    def __init__(self, object, tweenInfo, target, thread = None) -> None:
        self.target_object = object
        self.tweenInfo = tweenInfo
        self.target_property = target
        self.thread = thread if thread else GlobalTweenThread

        self.start_time = 0

        self.Completed = TweenEvent("Completed")
        self.TweenStarted = TweenEvent("TweenStarted")
        self.StartCalled = TweenEvent("StartCalled")

        if self.thread is None:
            _print_warning("RuntimeWarning", "Either the argument thread is None or TweenService has not been initialized")
        elif not isinstance(self.thread, TweenThread):
            raise ValueError(f"Invalid thread argument. It must be TweenThread, not a {self.thread.__class__.__name__}.")

    def GetTweenInfo(self):
        return TweenInfo(self.tweenInfo)
    
    def GetTweenInfoData(self, key):
        return self.GetTweenInfo().get(key)  

    def start(self):
        if not self.thread: raise RuntimeError("TweenService has not been initialized.")

        return self
    
    def update(self):
        for attr_n, val in self.target_property.items():
            pass

class GroupTweenHandler(TweenHandler):
    def __init__(self) -> None:
        pass

class TweenThread:
    def __init__(self, cycles = 60) -> None:
        self.thread = Thread(target=self.__update_wrap__, args=(self,), daemon=True)
        self.cycles = cycles
        self.stopped = False

        self.items: deque[TweenHandler] = deque()

    def get_items(self): return self.items
    def add_item(self, tw): self.items.append(tw)

    @staticmethod
    def __update_wrap__(self_obj):
        while not self_obj.stopped:
            st = get_time()
            self_obj.update()
            sleep(max(1 / self_obj.cycles - (get_time() - st), 0))

    def update(self):
        for tw_obj in self.items.copy(): tw_obj.update()

    def stop(self): 
        self.stopped = True
        return self
    
    def start(self): 
        self.stopped = False
        if not self.thread.is_alive(): self.thread.start()
        return self

def create_main_thread(cycles = 60):
    global GlobalTweenThread
    GlobalTweenThread = TweenThread(cycles)
    return GlobalTweenThread

def init(cycles = 60):
    thread = create_main_thread(cycles)
    thread.start()
    return thread