from collections import deque
from typing import Sequence, Any
from time import time as get_time, sleep
from threading import Thread
from TweenService.Easings import Linear
from operator import index as get_index

DEFAULT_TWEEN_TIME = 1
DEFAULT_TWEEN_STYLE = Linear
DEFAULT_TWEEN_DELAY = 0
DEFAULT_TWEEN_REPEAT_COUNT = 0
DEFAULT_TWEEN_REVERSES = False

TWEEN_EVENT_TYPE_DEFAULT = 0
TWEEN_EVENT_TYPE_ONCE = 1

TWEEN_METHOD_DICT = 0
TWEEN_METHOD_LIST = 1

_default_kpdict: dict | None = None

def _print_warning(type, message):
    print("\033[93m" + type + ": " + message + "\033[0m")

def _ival(t):
    if hasattr(t, "__float__"): return float(t)
    return int(t)

def _get_iter(obj, index):
    i = 0
    for x in obj:
        if i == index: return x
        i += 1

def _get_item(item, name, attr = False) -> Any:
    if attr: return getattr(item, name)
    if hasattr(item, "__getitem__"): return item[name]
    if hasattr(item, "__iter__"): return _ival(_get_iter(item, name))
    return getattr(item, name)

def _set_item(item, name, value, attr = False):
    if hasattr(item, "__setitem__") and not attr: item[name] = value
    else: setattr(item, name, value) 

def _ap_cond(m, f, a, b, key):
    # print("COND", m, a, b, key)
    sa = _get_item(a, key)
    sb = _get_item(b, key)
    attr_m = isinstance(a, dict) and not isinstance(m, dict)
    sm = _get_item(m, key, attr_m)
    if isinstance(sa, dict):
        _deep_apply_dict(sm, f, sa, sb)
    elif hasattr(sm, "__setitem__"):
        _deep_apply_list(sm, f, sa, sb)
    else:
        # print("APPLYING", a, b, sa, sb)
        if hasattr(sa, "__iter__"):
            result = tuple(f(sa[i], sb[i]) for i, _ in enumerate(sb))
        else:
            result = f(sa, sb)
        
        # print("RESULT", result)
        _set_item(m, key, result, attr_m)

def _deep_apply_list(m, f, a, b):
    for t, _ in enumerate(m):
        _ap_cond(m, f, a, b, t)

def _deep_apply_dict(m, f, a, b):
    for t in a:
        _ap_cond(m, f, a, b, t)

def _cp_cond(_m, _t, key):
    attr_m = isinstance(_t, dict) and not isinstance(_m, dict)
    sm = _get_item(_m, key, attr_m)
    st = _get_item(_t, key)
    if isinstance(st, dict):
        return _deep_copy_dict(sm, st)
    elif hasattr(sm, "__iter__"):
        if hasattr(sm, "__setitem__"):
            return _deep_copy_list(sm, st)
        else:
            return tuple(_ival(_get_item(sm, i)) for i in range(len(tuple(sm))))
    return _ival(sm)

def _deep_copy_dict(m, t):
    res = {}
    for key in t:
        res[key] = _cp_cond(m, t, key)
    return res

def _deep_copy_list(m, t):
    res = []
    for i in range(len(tuple(t))):
        res.append(_cp_cond(m, t, i))
    return res


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
            f"[TweenEvent:{self.name}] Warning",
            f"Cannot find function {func} to Disconnect."
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

def start_wrapper(self, delay):
    sleep(delay)    
    self._start()

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
        self.Step = TweenEvent("Step")

        self.start_time = 0
        self.running = False

        self._original_values = {}

        self.method = -1

        if globals()['_default_kpdict'] is None:
            global _default_kpdict
            _default_kpdict = {name.lower(): eval("DEFAULT_TWEEN_" + name) for name in 
                               ("TIME", "STYLE", "DELAY", "REPEAT_COUNT", "REVERSES")}

        if (fl := self.flags.get("force_method")) is not None: self.method = fl
        else:
            if isinstance(self.target, dict):
                self.method = 0
            elif hasattr(self.object, "__setitem__"):
                self.method = 1

        print("[Debug]: Method", self.method)

    def GetTweenInfo(self) -> TweenInfo:
        return TweenInfo(self.tweenInfo)

    def GetTweenInfoData(self, key):
        return self.GetTweenInfo().get(key)

    def _gt_tw_dt(self, key):
        return self.tweenInfo.get(key, _default_kpdict[key])    # type: ignore

    def _start(self):
        if self.thread is None:
            raise RuntimeError("Thread is None")

        if self.method == 1:
            self._original_values = _deep_copy_list(self.object, self.target)
        else:
            self._original_values = _deep_copy_dict(self.object, self.target)

        print("[Debug]: Original Values:", self._original_values)
        # raise BaseException("Stopped for debugging")

        self.running = True
        self.start_time = get_time()
        self.thread.add_item(self)
        self.TweenStarted.Fire(self.start_time)

    def start(self):
        self.StartCalled.Connect(get_time())
        if (delay := self.GetTweenInfoData("delay")) > 0:
            Thread(daemon=True, target=start_wrapper, args=(self, delay)).start()
        else:
            self._start()

    def update(self) -> bool | None:
        ti = get_time()
        if ti - self.start_time > self._gt_tw_dt("time"):
            if self.method == 1:
                _deep_apply_list(self.object, (lambda _, x: _ival(x)), self._original_values, self.target)
            elif self.method == 0:
                _deep_apply_dict(self.object, (lambda _, x: _ival(x)), self._original_values, self.target)
            self.Completed.Fire(ti)

            return True
        t = self._gt_tw_dt("style")(ti - self.start_time) / self._gt_tw_dt("time")
        funcc = lambda _a, _b: _ival(_a) + (_ival(_b) - _ival(_a)) * t

        if self.method == 1:
            _deep_apply_list(self.object, funcc, self._original_values, self.target)
        elif self.method == 0:
            _deep_apply_dict(self.object, funcc, self._original_values, self.target)
        self.Step.Fire(t)


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
            sm = get_time()
            self_obj.update()
            sleep(max(1 / self_obj.cycles - (get_time() - sm), 0))

    def update(self):
        for tw_obj in self.items.copy():
            completed = tw_obj.update()
            if completed == True:
                self.items.remove(tw_obj)

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
