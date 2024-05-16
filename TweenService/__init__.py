from typing import TypedDict, NotRequired, overload
from collections import deque
from time import time as get_time, sleep
from threading import Thread
from TweenService.Easings import Linear

number = int | float

def print_warning(type, message):
    print("\033[93m" + type + ": " + message + "\033[0m")

class TweenInfo_T(TypedDict):
    time: NotRequired[number]
    style: NotRequired[str]
    delay: NotRequired[number]
    repeat_count: NotRequired[int]
    reverses: NotRequired[bool]

class TweenInfo:
    def __init__(self, time = 1, style = None, delay = 0, repeat_count = 0, reverses = False):
        if isinstance(time, dict):  # overloading the worse way possible
            self.time = time.get("time", 1)
            self.style = time.get("style", Linear)
            self.delay = time.get("delay", 0)
            self.repeat_count = time.get("repeat_count", 0)
            self.reverses = time.get("reverses", False)
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

GlobalTweenThread = None

class TweenHandler:
    def __init__(self, object, tweenInfo, target, thread = None) -> None:
        self.target_object = object
        self.tweenInfo = tweenInfo
        self.target_property = target
        self.thread = thread if thread else GlobalTweenThread

        self.start_time = None

        if self.thread is None:
            print_warning("RuntimeWarning", "Either the argument thread is None or TweenService has not been initialized")
        elif not isinstance(self.thread, TweenThread):
            raise ValueError(f"Invalid thread argument. It must be TweenThread, not a {self.thread.__class__.__name__}.")

    def start(self):
        if not self.thread: raise RuntimeError("TweenService has not been initialized.")
        self.start_time = get_time()
        self.thread.add_item(self)
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

def init(cycles = 60):
    global GlobalTweenThread
    GlobalTweenThread = TweenThread(cycles)
    GlobalTweenThread.start()