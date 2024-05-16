import TweenService
from TweenService.Easings import EaseInExpo

t = TweenService.TweenHandler(1, {}, {})
print(t.start())

import pygame as pg 

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (680, 420)
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock() 

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT: running = False 

    screen.fill((255, 255, 255)) 

    pg.display.flip()
    clock.tick(60)