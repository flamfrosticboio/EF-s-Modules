"""A essential module containing a basic delay only"""

from threading import Thread
from typing import Callable
from time import sleep

def basic_delay(time: float, func: Callable[..., None], *args, **kwargs):
    """Does a basic delay for simple calls. This function does not require the module to initialize."""
    def wrapper(): 
        sleep(time)
        func(*args, **kwargs)
    Thread(daemon=True, target=wrapper).start()