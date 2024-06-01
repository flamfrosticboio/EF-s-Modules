"""A module for timing execution. Uses threading to achieve this"""

from typing import Callable, Iterable, overload, Never, Iterator, Any
from threading import Thread
from time import time as get_time, sleep

def basic_delay(time: float, func: Callable[..., None], *args, **kwargs):
    """Does a basic delay for simple calls. This function does not require the module to initialize."""
    def wrapper(): 
        sleep(time)
        func(*args, **kwargs)
    Thread(daemon=True, target=wrapper).start()


class TimingInterface:
    """An interface to control your timing functions."""
    def __init__(self, func_ptr, thread) -> None:
        self.ptr = func_ptr
        self.thr: TimingThread = thread

    def stop(self) -> Callable:
        """Stops and returns the original function pointer. Returns None if function cannot be found."""
        return self.thr.items.pop(self.ptr, None)  # type: ignore


class TimingThread:
    """A custom timing thread. Note: This did not inherit Thread from threading."""
    def __init__(self) -> None:
        self.thread: Thread = Thread(daemon=True, target=self._update_wrapper)
        self.items: dict[Callable | Iterable[Callable], Callable] = {}

    def start(self) -> None: 
        """Starts the thread."""
        self.thread.start()

    def _update_wrapper(self):
        while True: self.update()

    def update(self) -> None:
        for func_key, delay_func in self.items.copy().items():
            finished = delay_func()
            if finished: self.items.pop(func_key); print("DONE!", func_key)
        sleep(0)

_main_delay_thread: TimingThread | None = None

def _error_init() -> Never: raise RuntimeError("Timing module not yet initialized")

_get_len = lambda iterable: sum(1 for _ in iterable)
_safe_next = lambda item: next(item, None) if isinstance(item, Iterator) else item

def get_init() -> bool:
    return _main_delay_thread is not None

def delay(time: int | float, func: Callable[..., Any], _thread: TimingThread | None = None, *args, **kwargs):
    """Sets a delay to execute a function."""

    if _thread is None: _thread = _main_delay_thread
    if not isinstance(_thread, TimingThread): _error_init()

    start_time = get_time()
    def delay_func():
        if get_time() - start_time < time: return False
        func(*args, **kwargs)
        return True
    _thread.items[func] = delay_func

    return TimingInterface(func, _thread)

def interval(interval: int | float, func: Callable[..., Any], repeats: int = 0, 
             execute_first: bool = False, _thread: TimingThread | None = None, 
             *args, **kwargs) -> TimingInterface:
    """Execute function at an interval specified by repeats. If repeats is lesser than 0, it will be infinite."""

    if _thread is None: _thread = _main_delay_thread
    if not isinstance(_thread, TimingThread): _error_init()

    last_time = get_time()
    repeats += 1 
    def delay_func():
        nonlocal last_time, execute_first
        if execute_first:
            execute_first = False
            func(*args, **kwargs)
        if get_time() - last_time < interval: return False
        nonlocal repeats
        last_time = get_time()
        repeats += -1  
        func(*args, **kwargs)
        return repeats == 0
    _thread.items[func] = delay_func

    return TimingInterface(func, _thread)

@overload
def sequenced_delay(interval: int | float, functions: Iterable[Callable[..., Any]],
                    repeats: int = 0, execute_first: bool = False,
                    _thread: TimingThread | None = None, *args, **kwargs) -> TimingInterface: ...

@overload
def sequenced_delay(interval: Iterable[int | float], functions: Iterable[Callable[..., Any]],
                    repeats: int = 0, execute_first: bool = False, _thread: TimingThread | None = None,
                    *args, **kwargs) -> TimingInterface: ...

def sequenced_delay(interval, functions, repeats = 0, execute_first = False, 
                    _thread: TimingThread | None = None, *args, **kwargs):
    """Executes a series of functions in a sequence with specified delay/s. If repeats is lesser than 0,
     it will be infinite."""
    
    if _thread is None: _thread = _main_delay_thread
    if not isinstance(_thread, TimingThread): _error_init()

    intv_iter = isinstance(interval, Iterable)
    if intv_iter and _get_len(interval) != _get_len(functions): 
        raise ValueError("Length of delay sequence and functions is not the same.")
    
    _delay_iter = iter(interval) if intv_iter else interval
    _func_iter = iter(functions)
    _next_delay = _safe_next(_delay_iter)

    repeats += 1    # offset

    if _next_delay is None:
        print("[Delay][Warning]:", "Iterable is empty especially delay. This will cancel this operation!")
        return True
    
    _target_time = get_time() + _next_delay
    def delay_func():
        nonlocal _target_time, execute_first

        if not execute_first and get_time() < _target_time: return False
        execute_first = False

        nonlocal repeats, _func_iter, _delay_iter

        _func = _safe_next(_func_iter)
        if _func is not None: _func(*args, **kwargs)

        next_delay = _safe_next(_delay_iter)
        if next_delay is None or _func is None: 
            repeats += -1
            if repeats == 0: return True
            _delay_iter = iter(interval) if intv_iter else interval
            _func_iter = iter(functions)
            _target_time = get_time() + _safe_next(_delay_iter)  # type: ignore
            next(_func_iter)(*args, **kwargs)
        else:
            _target_time = get_time() + next_delay
    _thread.items[functions] = delay_func

    return TimingInterface(functions, _thread)

def init() -> None:
    global _main_delay_thread
    _main_delay_thread = TimingThread()
    _main_delay_thread.start()

def get_main_thread() -> TimingThread | None:
    return _main_delay_thread