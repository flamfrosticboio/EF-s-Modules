"""A module containing all easing defs for TweenService. For more information, visit https://easings.net/"""

from typing import Callable, TypeAlias
import math as Math
number = int | float

# Defining Constants
_c1 = 1.70158
_c2 = _c1 * 1.525
_c3 = _c1 + 1
_c4 = (2 * Math.pi) / 3
_c5 = (2 * Math.pi) / 4.5
_n1 = 7.5625
_d1 = 2.75

EasingFunction: TypeAlias = Callable[[number], float]     # A typing alias

def Linear(progress: number) -> number:
    return progress

def EaseInSine(progress: number) -> number:
    return 1 - Math.cos((progress * Math.pi) / 2)

def EaseOutSine(progress: number) -> number:
    return Math.sin((progress * Math.pi) / 2)

def EaseInOutSine(progress: number) -> number:
    return -(Math.cos(Math.pi * progress) - 1) / 2

def EaseInQuad(progress: number) -> number:
    return progress * progress

def EaseOutQuad(progress: number) -> number:
    return 1 - (1 - progress) * (1 - progress)

def EaseInOutQuad(progress: number) -> number:
    if progress < 0.5: return 2 * progress * progress
    return 1 - Math.pow(-2 * progress + 2, 2) / 2

def EaseInCubic(progress: number) -> number:
    return progress * progress * progress

def EaseOutCubic(progress: number) -> number:
    return 1 - Math.pow(1 - progress, 3)

def EaseInOutCubic(progress: number) -> number:
    if progress < 0.5: return 4 * progress * progress * progress
    return 1 - Math.pow(-2 * progress + 2, 3) / 2

def EaseInQuart(progress: number) -> number:
    return progress * progress * progress * progress

def EaseOutQuart(progress: number) -> number:
    return 1 - Math.pow(1 - progress, 4)

def EaseInOutQuart(progress: number) -> number:
    if progress < 0.5: return 8 * progress * progress * progress * progress
    return 1 - Math.pow(-2 * progress + 2, 4) / 2

def EaseInQuint(progress: number) -> number:
    return progress * progress * progress * progress * progress

def EaseOutQuint(progress: number) -> number:
    return 1 - Math.pow(1 - progress, 5)

def EaseInOutQuint(progress: number) -> number:
    if progress < 0.5: return 16 * progress * progress * progress * progress * progress
    return 1 - Math.pow(-2 * progress + 2, 5) / 2

def EaseInExpo(progress: number) -> number:
    if progress == 0: return 0
    return Math.pow(2, 10 * progress - 10)

def EaseOutExpo(progress: number) -> number:
    if progress == 1: return 1
    return 1 - Math.pow(2, -10 * progress)

def EaseInOutExpo(progress: number) -> number:
    if progress == 0: return 0
    elif progress == 1: return 1
    elif progress < 0.5: return Math.pow(2, 20 * progress - 10) / 2
    return (2 - Math.pow(2, -20 * progress + 10)) / 2

def EaseInCirc(progress: number) -> number:
    return 1 - Math.sqrt(1 - Math.pow(progress, 2))

def EaseOutCirc(progress: number) -> number:
    return Math.sqrt(1 - Math.pow(progress - 1, 2))

def EaseInOutCirc(progress: number) -> number:
    if progress < 0.5: return (1 - Math.sqrt(1 - Math.pow(2 * progress, 2))) / 2
    return (Math.sqrt(1 - Math.pow(-2 * progress + 2, 2)) + 1) / 2

def EaseInBack(progress: number) -> number:
    return _c3 * progress * progress * progress - _c1 * progress * progress

def EaseOutBack(progress: number) -> number:
    return 1 + _c3 * Math.pow(progress - 1, 3) + _c1 * Math.pow(progress - 1, 2)

def EaseInOutBack(progress: number) -> number:
    if progress < 0.5: return (Math.pow(2 * progress, 2) * ((_c2 + 1) * 2 * progress - _c2)) / 2
    return (Math.pow(2 * progress - 2, 2) * ((_c2 + 1) * (progress * 2 - 2) + _c2) + 2) / 2

def EaseInElastic(progress: number) -> number:
    if progress == 0: return 0
    elif progress == 1: return 1
    return -Math.pow(2, 10 * progress - 10) * Math.sin((progress * 10 - 10.75) * _c4)

def EaseOutElastic(progress: number) -> number:
    if progress == 0: return 0
    elif progress == 1: return 1
    return Math.pow(2, -10 * progress) * Math.sin((progress * 10 - 0.75) * _c4) + 1

def EaseInOutElastic(progress: number) -> number:
    if progress == 0: return 0
    elif progress == 1: return 1
    elif progress < 0.5: return -(Math.pow(2, 20 * progress - 10) * Math.sin((20 * progress - 11.125) * _c5)) / 2
    return (Math.pow(2, -20 * progress + 10) * Math.sin((20 * progress - 11.125) * _c5)) / 2 + 1

def EaseOutBounce(progress: number) -> number:
    if (progress < 1 / _d1): return _n1 * progress * progress
    elif (progress < 2 / _d1): 
        progress -= 1.5
        return _n1 * (progress / _d1) * progress + 0.75
    elif (progress < 2.5 / _d1): 
        progress -= 2.25
        return _n1 * (progress / _d1) * progress + 0.9375
    progress -= 2.625
    return _n1 * (progress / _d1) * progress + 0.984375

def EaseInBounce(progress: number) -> number:
    return 1 - EaseOutBounce(1 - progress)
   
def EaseInOutBounce(progress: number) -> number:
    if progress < 0.5: return (1 - EaseOutBounce(1 - 2 * progress)) / 2
    return (1 + EaseOutBounce(2 * progress - 1)) / 2
