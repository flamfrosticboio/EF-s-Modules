from collections import deque
from typing import Sequence
from time import time as get_time, sleep
from threading import Thread
from TweenService.Easings import Linear

DEFAULT_TWEEN_TIME = 1
DEFAULT_TWEEN_STYLE = Linear
DEFAULT_TWEEN_DELAY = 0
DEFAULT_TWEEN_REPEAT_COUNT = 0
DEFAULT_TWEEN_REVERSES = False

TWEEN_EVENT_TYPE_DEFAULT = 0
TWEEN_EVENT_TYPE_ONCE = 1

TWEENFLAG_USE_CUSTOM_SEQUENCE = 0b00000001

_default_kpdict = {
    name.lower(): eval("DEFAULT_TWEEN_" + name)
    for name in ("TIME", "STYLE", "DELAY", "REPEAT_COUNT", "REVERSES")
}


def _print_warning(type, message):
    print("\033[93m" + type + ": " + message + "\033[0m")


def _has_method(obj, name):
    name = "__" + name + "__"
    return hasattr(obj, name) and callable(getattr(obj, name))


def _ival_ex(t):
    if hasattr(t, "__tw_use_value__"):
        if callable(getattr(t, "__tw_use_value__")):
            return getattr(t, getattr(t, "__tw_use_value__")())
        return getattr(t, getattr(t, "__tw_use_value__"))
    return t


def _apply_val(a, b, t):
    if isinstance(a, tuple):
        res = tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
        return res
    else:
        a, b = _ival_ex(a), _ival_ex(b)
        return a + (b - a) * t


def _get_key_ex(obj, key):
    if _has_method(obj, "getitem"):
        return obj[key]
    elif _has_method(obj, "iter") and isinstance(key, int):
        i = 0
        for item in obj:
            if i == key:
                return item
            i += 1


class TweenInfo:
    def __init__(self, time=1, style=None, delay=0, repeat_count=0, reverses=False):
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
        kwargs = [f"{n}={m}" for n, m in self.__dict__.items()]
        kwargs[1] = f"style={self.style.__name__}"  # simple fix to serialize style name
        return f"{self.__class__.__name__}({', '.join(kwargs)})"

    def to_dict(self):
        return dict(self.__dict__.items())

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


GlobalTweenThread = None


class TweenEvent:
    def __init__(self, name):
        self.events = deque()
        self.name = name

    def _wrap_func(self, func, type=TWEEN_EVENT_TYPE_DEFAULT):
        return (func, type)

    def Connect(self, func, append_left=False):
        func = self._wrap_func(func)
        if append_left == True:
            self.events.appendleft(func)
        else:
            self.events.append(func)

    def Disconnect(self, func):
        for _func, _t in self.events.copy():
            if _func == func:
                self.events.remove((_func, _t))
                return
        _print_warning(
            f"[TweenEvent:{self.name}] Warning: Cannot find function {func} to Disconnect."
        )

    def Once(self, func, append_left=False):
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


def get_iter_len(obj):
    length = 0
    for _ in obj:
        length += 1
    return length


def get_iter(obj, flags):
    if isinstance(obj, (list, tuple)):
        return range(len(obj))
    if flags.get("use_range"):
        return range(len(obj) if _has_method(obj, "len") else get_iter_len(obj))
    return obj


class TweenHandler:
    def __init__(self, object, tweenInfo, target, thread=None, **flags) -> None:
        self.object = object
        self.tweenInfo = tweenInfo
        self.target = target
        self.thread = thread if thread else GlobalTweenThread
        self.flags = flags

        self.Completed = TweenEvent("Completed")
        self.TweenStarted = TweenEvent("TweenStarted")
        self.StartCalled = TweenEvent("StartCalled")

        self.start_time = 0
        self.running = False

        self._original_values = {}

    def GetTweenInfo(self) -> TweenInfo:
        return TweenInfo(self.tweenInfo)

    def GetTweenInfoData(self, key):
        return self.GetTweenInfo().get(key)

    def _gt_tw_dt(self, key):
        return self.tweenInfo.get(key, _default_kpdict[key])

    def _start(self):
        if isinstance(self.object, list):
            self._original_values = self.object.copy()
        elif isinstance(self.object, dict):
            for key in self.target:
                self._original_values[key] = self.object.get(key)
        elif _has_method(self.object, "setitem") and _has_method(
            self.object, "getitem"
        ):
            for key in self.target:
                self._original_values[key] = self.object[key]
        else:
            for key in self.target:
                self._original_values[key] = getattr(self.object, key)

        print(self._original_values)

        self.running = True
        self.start_time = get_time()
        self.thread.add_item(self)
        self.TweenStarted.Fire(get_time())

    def start(self):
        self.StartCalled.Connect(get_time())
        if (delay := self.GetTweenInfoData("delay")) > 0:

            def wrapper():
                sleep(delay)
                self._start()

            Thread(daemon=True, target=wrapper).start()
        else:
            self._start()

    def update(self) -> bool:
        if (t := get_time()) - self.start_time > self._gt_tw_dt("time"):
            self.Completed.Fire(t)
            return True
        t = self._gt_tw_dt("style")(t - self.start_time) / self._gt_tw_dt("time")

        for key in get_iter(self.target, self.flags):
            a = self._original_values[key]
            b = _get_key_ex(self.target, key)
            if isinstance(self.object, (list, dict)):
                self.object[key] = _apply_val(a, b, t)
            else:
                setattr(self.object, key, _apply_val(a, b, t))


class GroupTweenHandler(TweenHandler):
    def __init__(self) -> None:
        pass


class TweenThread:
    def __init__(self, cycles=60) -> None:
        self.thread = Thread(target=self.__update_wrap__, args=(self,), daemon=True)
        self.cycles = cycles
        self.stopped = False

        self.items: deque[TweenHandler] = deque()

    def get_items(self):
        return self.items

    def add_item(self, tw):
        self.items.append(tw)

    @staticmethod
    def __update_wrap__(self_obj):
        while not self_obj.stopped:
            st = get_time()
            self_obj.update()
            sleep(max(1 / self_obj.cycles - (get_time() - st), 0))

    def update(self):
        for tw_obj in self.items.copy():
            completed = tw_obj.update()
            if completed == True:
                self.items.remove(tw_obj)
                print("Done!")

    def stop(self):
        self.stopped = True
        return self

    def start(self):
        self.stopped = False
        if not self.thread.is_alive():
            self.thread.start()
        return self


def create_main_thread(cycles=60):
    global GlobalTweenThread
    GlobalTweenThread = TweenThread(cycles)
    return GlobalTweenThread


def init(cycles=60):
    thread = create_main_thread(cycles)
    thread.start()
    return thread
