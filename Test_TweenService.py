import pygame as pg
import TweenService
from threading import Thread
from time import sleep
from test_classes import *

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
    Frame((10, 100), (50, 50), (255, 0, 0)),
    Frame((10, 160), (50, 50), (255, 0, 0)),
]

pLoopFunc = None
item_index = 0
completed = False

item_a = None
i = 0

def attach_frame(tweenEvent, frame, func):
    tweenEvent.Connect(func(frame))

# Our test case
test_data = {
    "Method Test": {
        "data": [
            # List type tests
            ("allFrames[0].rect", "{}, [100, 100, 1, 1]"),
            ("[20, 20]", "{}, (100, 100)"),
            ("[20, 20]", "{}, LinkedList(100, 100)", ""),
            ("LinkedList_Extended(20, 20)", "{}, LinkedList(100, 100)"),
            ("[[20, 20], [40, 40], [[50, 60], [70, 80]], [90, 20]]", "{}, [[10, 10], [10, 500], [[10, 11], [12, 13]], [14, 15]]"),
            ("[LinkedList_Extended(20, 20), LinkedList_Extended(40, 40)]", "{}, (LinkedList(100, 100), LinkedList(20, 20))"),
            
            # Dict type tests
            ("{'va': [20, 20]}", "{}, {'va': [100, 100]}"),
            ("{'va': [20, 20], 'vb': {'a': [10, 20], 'b': 4}}", "{}, {'vb': {'a': [400, 400], 'b': 200}}"),
            ("{'va': LinkedList_Extended(10, 10)}", "{}, {'va': LinkedList(200, 200)}"),
            ("{'va': [20, 20], 'vb': {'a': LinkedList_Extended(10, 10), 'b': Node(24)}}", "{}, {'va': [40, 40], 'vb': {'a': LinkedList(200, 200), 'b': Node(200)}}"),
            
            # Attribute type tests
            ("allFrames[0].rect", "{}, {'topleft': [200, 200], 'size': [200, 200]}"),
            ("DataWrapper(allFrames[0].rect)", "{}, {'values': [200, 200, 100, 100]}"),
            # ("DataWrapper(allFrames[0].rect)", "{}, {'values': {'topleft': [200, 200], 'size': [100, 100]}}"),
            ],
        "command": [
            "globals()['completed'] = False",
            "item_a = %s",
            "allFrames[0].rect.topleft = (10, 10)",
            "allFrames[0].rect.size = (50, 50)",
            "x = TweenService.TweenHandler(item_a, %s)",
            "x.Completed.Connect(lambda _: allFrames[0].image.fill((0, 255, 0)))",
            "x.TweenStarted.Connect(lambda _: allFrames[0].image.fill((255, 0, 0)))",
            "x.Completed.Connect(lambda _: exec('globals()[\"completed\"] = True'))",
            "x.Completed.Connect(lambda _: print('Final values:', allFrames[0].rect.topleft, allFrames[0].rect.size))",
            "globals()['item_a'] = item_a",
            # "%s",
            "x.start()",
        ],
        "loop_command": [
            "allFrames[0].rect.topleft = item_a"
        ],
        "interval": 0.5,
    },
    "Easing Tests": {
        "data": [["Sine"], ["Quad"], ["Cubic"], ["Quart"], ["Quint"], 
                 ["Expo"], ["Circ"], ["Back"], ["Elastic"], ["Bounce"]],
        "command": [
            "globals()['completed'] = False",
            "item_a = allFrames[0].rect",
            "allFrames[0].rect.topleft = (10, 10)",
            "allFrames[0].rect.size = (50, 50)",
            "allFrames[1].rect.topleft = (10, 120)",
            "allFrames[1].rect.size = (50, 50)",
            "allFrames[2].rect.topleft = (10, 220)",
            "allFrames[2].rect.size = (50, 50)",
            "for i, t in enumerate(('In', 'Out', 'InOut')):"
            " x=TweenService.TweenHandler(allFrames[i].rect, {'style': eval(f'TweenService.Easings.Ease{t}%s')}, {'topleft': [450, 200 + (60 * i)], 'size': [20, 20]});"
            " attach_frame(x.Completed, i, lambda x: lambda y: allFrames[x].image.fill((0, 255, 0)));"
            " attach_frame(x.TweenStarted, i, lambda x: lambda y: allFrames[x].image.fill((255, 0, 0)));"
            " x.Completed.Connect(lambda _: exec('globals()[\"completed\"] = True'));"
            " x.start();",
            #"x.Completed.Connect(lambda _: print('Final values:', allFrames[0].rect.topleft, allFrames[0].rect.size))",
            "globals()['item_a'] = item_a",
            # "%s",
        ],
        "interval": 0.2,
    }
}

print("Tester 1.0 [Made by \\'ER']")

skip_test = ["Method Test"]

def tester():
    global pLoopFunc
    for test_data_name in test_data:
        if test_data_name in skip_test: continue

        contents = test_data[test_data_name]
        print("Now Executing:", test_data_name)
        for i in range(len(contents['data'])):
            print(">>", contents['data'][i])
            di = 0
            for cmd in contents['command']:
                if "%" in cmd:
                    # print(">", cmd % contents['data'][i][di])
                    if di < len(contents['data'][i]) and contents['data'][i][di]:
                        exec(cmd % contents['data'][i][di])
                    else:
                        exec(cmd)
                    di += 1
                else:
                    # print(">", cmd)
                    exec(cmd)
            while completed == False:
                sleep(0.1)
            sleep(contents.get("interval", 1))

Thread(daemon=True, target=tester).start()


running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    tween_thread_main.update()
    screen.fill((255, 255, 255))

    if pLoopFunc:
        for cmd in pLoopFunc:
            exec(cmd)
        
    if item_a:
        if isinstance(item_a, list):
            if len(item_a) < 3 and isinstance(item_a[0], (int, float)): allFrames[0].rect.topleft = item_a
        elif isinstance(item_a, (LinkedList, LinkedList_Extended)):
            allFrames[0].rect.topleft = item_a.get_values()
        elif isinstance(item_a, dict):
            if isinstance(item:=item_a.get("va"), LinkedList_Extended):
                allFrames[0].rect.topleft = item.get_values()
            else:
                allFrames[0].rect.topleft = item
        # print(item_a)

    for frame in allFrames:
        frame.render(screen)

    pg.display.flip()
    clock.tick(60)
