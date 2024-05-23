from collections import deque
from typing import Sequence
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

TWEEN_METHOD_ATTRIBUTE = 0
TWEEN_METHOD_LIST = 1
TWEEN_METHOD_DICT = 2

_default_kpdict = {
    name.lower(): eval("DEFAULT_TWEEN_" + name)
    for name in ("TIME", "STYLE", "DELAY", "REPEAT_COUNT", "REVERSES")
}


def _print_warning(type, message):
    print("\033[93m" + type + ": " + message + "\033[0m")


def _has_method(obj, name):
    name = "__" + name + "__"
    return hasattr(obj, name) and callable(getattr(obj, name))


def _has_methods(obj, _t):
    return all(_has_method(obj, name) for name in _t)


def _ival(t):
    if _has_method(t, "int"):
        return int(t)
    elif _has_method(t, "float"):
        return float(t)
    return t


def _get_key_ex(obj, key):
    if _has_method(obj, "getitem"):
        return obj[key]
    elif _has_method(obj, "iter") and isinstance(key, int):
        i = 0
        for item in obj:
            if i == key:
                return item
            i += 1


def get_iter_len(obj):
    if _has_method(obj, "len"):
        return len(obj)
    length = 0
    for _ in obj:
        length += 1
    return length


def _class(instance):
    return instance.__class__


def _deep_apply_attr(main, func, a, b):
    for key in a:
        mattr = getattr(main, key)
        if _has_method(mattr, "iter"):
            if isinstance(mattr, dict):
                _deep_apply_dict(mattr, func, a[key], b[key])
            elif _has_method(mattr, "setitem"):
                _deep_apply_list(mattr, func, a[key], b[key])
            else:
                setattr(
                    main,
                    key,
                    tuple(
                        func(_get_key_ex(a[key], i), _get_key_ex(b[key], i))
                        for i in range(get_iter_len(mattr))
                    ),
                )
        else:
            setattr(main, key, func(a[key], b[key]))

def _deep_copy_attr(_m, _tar_d):
    res = {}
    for key in _tar_d:
        item = getattr(_m, key)
        if _has_method(item, "iter"):
            if isinstance(item, dict):
                res[key] = _deep_copy_dict(item, _tar_d[key])
            elif _has_method(item, "getitem"):
                res[key] = _deep_copy_list(item)
            else:
                res[key] = _deep_copy_attr(item, _tar_d[key])
        else:
            res[key] = _ival(item)
    return res

def _deep_copy_list(_list):
    res = []
    for item in _list:
        if _has_method(item, "iter"):
            res.append(_deep_copy_list(item))
        else:
            res.append(_ival(item))
    return res


def _deep_apply_list(main, func, a, b):
    for index, item in enumerate(main):
        if _has_method(item, "iter"):
            _deep_apply_list(item, func, _get_key_ex(a, index), _get_key_ex(b, index))
        elif _has_method(main, "setitem"):
            main[index] = func(_get_key_ex(a, index), _get_key_ex(b, index))
        else:
            raise TypeError(
                f"Cannot apply value to non-mutable or no item assignment support class {main.__class__.__name__}."
            )


def _deep_same_list(a, b):
    if _has_method(a, "iter") and _has_method(b, "iter"):
        if get_iter_len(a) != get_iter_len(b):
            return False
        return all(_deep_same_list(sub1, sub2) for sub1, sub2 in zip(a, b))
    return isinstance(_ival(a), (int, float)) and isinstance(_ival(b), (int, float))


def _deep_copy_dict(_m, _tar_d):
    res = {}
    for key in _tar_d:
        item = _m[key]
        if _has_method(item, "iter"):
            if isinstance(item, dict):
                res[key] = _deep_copy_dict(item, _tar_d[key])
            else:
                res[key] = _deep_copy_list(item)
        else:
            res[key] = _ival(item)
    return res


def _deep_apply_dict(main, func, a, b):
    for key in a:
        if _has_method(main[key], "iter"):
            if isinstance(main[key], dict):
                _deep_apply_dict(main[key], func, a[key], b[key])
            else:
                _deep_apply_list(main[key], func, a[key], b[key])
        else:
            main[key] = func(a[key], b[key])


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


def get_iter(obj, flags):
    if isinstance(obj, (list, tuple)):
        return range(len(obj))
    if flags.get("use_range"):
        return range(len(obj) if _has_method(obj, "len") else get_iter_len(obj))
    return obj


def _get_item_iter(obj, index):
    for x in obj:
        if get_index(x) == index:
            return _ival(x)
    raise IndexError(f"Index out of range. index={index}")


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

        self.method = TWEEN_METHOD_ATTRIBUTE

        if (fl := self.flags.get("force_method")) is not None:
            self.method = fl
        else:
            if (
                _has_methods(self.object, ("setitem", "getitem"))
                and _has_method(self.target, "iter")
                and not issubclass(_class(self.target), dict)
            ):
                self.method = TWEEN_METHOD_LIST

            elif issubclass(_class(self.object), dict) and issubclass(
                _class(self.target), dict
            ):
                self.method = TWEEN_METHOD_DICT

            elif issubclass(_class(self.target), dict):
                self.method = TWEEN_METHOD_ATTRIBUTE

        if self.method == TWEEN_METHOD_LIST:
            if not _deep_same_list(self.object, self.target):
                raise ValueError(
                    f"Both object[{self.object.__class__.__name__}] and target[{self.target.__class__.__name__}] don't have the same structure."
                )

        print("[Debug]: Method", self.method)

    def GetTweenInfo(self) -> TweenInfo:
        return TweenInfo(self.tweenInfo)

    def GetTweenInfoData(self, key):
        return self.GetTweenInfo().get(key)

    def _gt_tw_dt(self, key):
        return self.tweenInfo.get(key, _default_kpdict[key])

    def _start(self):
        if self.method == TWEEN_METHOD_LIST:
            self._original_values = _deep_copy_list(self.object)
        elif self.method == TWEEN_METHOD_DICT:
            self._original_values = _deep_copy_dict(self.object, self.target)
        elif self.method == TWEEN_METHOD_ATTRIBUTE:
            self._original_values = _deep_copy_attr(self.object, self.target)

        # _deep_apply_list(self.object, lambda *args: print(*args))

        print("Original Values:", self._original_values)

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
        ti = get_time()
        if ti - self.start_time > self._gt_tw_dt("time"):
            if self.method == TWEEN_METHOD_LIST:
                _deep_apply_list(
                    self.object,
                    (lambda a, b: _ival(b)),
                    self._original_values,
                    self.target,
                )
            elif self.method == TWEEN_METHOD_DICT:
                _deep_apply_dict(
                    self.object,
                    (lambda a, b: _ival(b)),
                    self._original_values,
                    self.target,
                )
            elif self.method == TWEEN_METHOD_ATTRIBUTE:
                for key in self.target:
                    self._original_values[key] = setattr(
                        self.object, key, self.target[key]
                    )
            self.Completed.Fire(ti)

            return True
        t = self._gt_tw_dt("style")(ti - self.start_time) / self._gt_tw_dt("time")
        funcc = lambda a, b: _ival(a) + (_ival(b) - _ival(a)) * t

        if self.method == TWEEN_METHOD_LIST:
            _deep_apply_list(self.object, funcc, self._original_values, self.target)
        elif self.method == TWEEN_METHOD_DICT:
            _deep_apply_dict(self.object, funcc, self._original_values, self.target)
        elif self.method == TWEEN_METHOD_ATTRIBUTE:
            _deep_apply_attr(self.object, funcc, self._original_values, self.target)
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
