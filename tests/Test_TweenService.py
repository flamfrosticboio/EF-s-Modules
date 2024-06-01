import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)

import pygame as pg
from src import TweenService
from src.TweenService import Easings
from threading import Thread
from time import sleep
from tests.test_classes import *
import EFLTester

tween_thread_main = TweenService.create_main_thread()

class Frame:
    def __init__(self, pos, size, color):
        self.image = pg.Surface(size)
        self.rect = pg.Rect(pos, size)
        self.image.fill(color)

    def render(self, surface):
        self.rect.w = max(self.rect.w, 10)
        self.rect.h = max(self.rect.h, 10)

        image = pg.Surface(self.rect.size)
        image.fill(self.image.get_at((0, 0)))
        surface.blit(image, self.rect)

def to_values(item: list[Node]):
    return [int(x) for x in item]


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (680, 420)
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

allFrames = [
    Frame((10, 10), (50, 50), (255, 0, 0)),
]

item_index = 0
completed = False

item_a = None
i = 0

def attach_frame(tweenEvent, frame, func):
    tweenEvent.Connect(func(frame))

# Our test case
test_data: dict[str, EFLTester.TestDataContents] = {
    "Method Test": {
        "data": [
            # List type tests
            {'a0': "allFrames[0].rect", 'a1': "{}, [100, 100, 1, 1]"},
            {'a0': "[20, 20]", 'a1': "{}, (100, 100)"},
            {'a0': "[20, 20]", 'a1': "{}, LinkedList(100, 100)"},
            {'a0': "LinkedList_Extended(20, 20)", 'a1': "{}, LinkedList(100, 100)"},
            {'a0': "[[20, 20], [40, 40], [[50, 60], [70, 80]], [90, 20]]", 'a1': "{}, [[10, 10], [10, 500], [[10, 11], [12, 13]], [14, 15]]"},
            {'a0': "[LinkedList_Extended(20, 20), LinkedList_Extended(40, 40)]", 'a1': "{}, (LinkedList(100, 100), LinkedList(20, 20))"},
            
            # Dict type tests
            {'a0': "{'va': [20, 20]}", 'a1': "{}, {'va': [100, 100]}"},
            {'a0': "{'va': [20, 20], 'vb': {'a': [10, 20], 'b': 4}}", 'a1': "{}, {'vb': {'a': [400, 400], 'b': 200}}"},
            {'a0': "{'va': LinkedList_Extended(10, 10)}", 'a1': "{}, {'va': LinkedList(200, 200)}"},
            {'a0': "{'va': [20, 20], 'vb': {'a': LinkedList_Extended(10, 10), 'b': Node(24)}}", 'a1': "{}, {'va': [40, 40], 'vb': {'a': LinkedList(200, 200), 'b': Node(200)}}"},
            
            # Attribute type tests
            {'a0': "allFrames[0].rect", 'a1': "{}, {'topleft': [200, 200], 'size': [200, 200]}"},
            {'a0': "DataWrapper(allFrames[0].rect)", 'a1': "{}, {'values': [200, 200, 100, 100]}"},
            
            # Combos
            {'a0': "[{'a': 10, 'b': [10, 20]}]", 'a1': "{}, [{'a': 100, 'b': [100, 200]}]"},
            {'a0': "{'a': [10, 20], 'b': {'c': [30, 40]}}", 'a1': "{}, {'a': [100, 200], 'b': {'c': [300, 400]}}"},
            {'a0': "[{'a': [{'b': [{'c': 10}]}]}]", 'a1': "{}, [{'a': [{'b': [{'c': 100}]}]}]"},
            {'a0': "[allFrames[0].rect]", 'a1': "{}, [{'topleft': [20, 30]}]"},
            {'a0': "[{'a': DataWrapper([{'b': allFrames[0].rect}])}]", 'a1': "{}, [{'a': {'values': [{'b': {'topleft': [10, 20]}}]}}]"},
            ],
        "commands": [
            "globals()['completed'] = False",
            "item_a = {a0}",
            "allFrames[0].rect.topleft = (10, 10)",
            "allFrames[0].rect.size = (50, 50)",
            "x = TweenService.TweenHandler(item_a, {a1})",
            "x.Completed.Connect(lambda _: allFrames[0].image.fill((0, 255, 0)))",
            "x.TweenStarted.Connect(lambda _: allFrames[0].image.fill((255, 0, 0)))",
            "x.Completed.Connect(lambda _: exec('globals()[\"completed\"] = True'))",
            "x.Completed.Connect(lambda _: print('Final values:', allFrames[0].rect.topleft, allFrames[0].rect.size, '\\n'))",
            "x.Step.Connect(lambda _: print('>', item_a))",
            "globals()['item_a'] = item_a",
            "x.start()",
        ],
        "interval": 1,
    },
    "Easing Tests": {
        "data": ["Sine", "Quad", "Cubic", "Quart", "Quint", 
                 "Expo", "Circ", "Back", "Elastic", "Bounce"],
        "commands": [
            "globals()['completed'] = False",
            "item_a = allFrames[0].rect",
            "allFrames[0].rect.topleft = (10, 10)",
            "allFrames[0].rect.size = (50, 50)",
            "allFrames[1].rect.topleft = (10, 120)",
            "allFrames[1].rect.size = (50, 50)",
            "allFrames[2].rect.topleft = (10, 220)",
            "allFrames[2].rect.size = (50, 50)",
            "for i, t in enumerate(('In', 'Out', 'InOut')):"
            " x=TweenService.TweenHandler(allFrames[i].rect, {{'style': eval(f'Easings.Ease{{t}}{}')}}, {{'topleft': [450, 200 + (60 * i)], 'size': [20, 20]}});"
            " attach_frame(x.Completed, i, lambda x: lambda y: allFrames[x].image.fill((0, 255, 0)));"
            " attach_frame(x.TweenStarted, i, lambda x: lambda y: allFrames[x].image.fill((255, 0, 0)));"
            " x.Completed.Connect(lambda _: exec('globals()[\"completed\"] = True'));"
            " x.start();",
            "globals()['item_a'] = item_a",
        ],
        "setup_commands": [
            "allFrames.append(Frame((10, 10), (50, 50), (255, 0, 0)))",
            "allFrames.append(Frame((10, 10), (50, 50), (255, 0, 0)))"
        ],
        "interval": 1.3,
    },
    "Special Commands": {
        'data': [
            "{'reverses': True}",
            "{'reverses': True, 'style': Easings.EaseInOutBounce}",
            "{'reverses': True, 'style': Easings.EaseInOutBack}",
            "{'repeat_count': 5, 'style': Easings.EaseInOutBack}",
            "{'repeat_count': 3, 'style': Easings.EaseInOutBack, 'reverses': True}",
        ],
        'commands': [
            "item_a = allFrames[0].rect",
            "allFrames[0].rect.topleft = (10, 10)",
            "allFrames[0].rect.size = (50, 50)",
            "x = TweenService.TweenHandler(item_a, {}, [200, 10, 20, 20])",
            "x.start()",
        ],
        'interval': 6
    }
}

skip_test = []

EFLTester.async_main(test_data, globals(), locals())


running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    tween_thread_main.update()
    screen.fill((255, 255, 255))

    for frame in allFrames:
        frame.render(screen)

    pg.display.flip()
    clock.tick(60)
