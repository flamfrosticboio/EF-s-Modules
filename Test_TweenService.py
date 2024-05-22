import pygame as pg 
import TweenService

tween_thread_main = TweenService.create_main_thread()

class Frame:
    def __init__(self, pos, size, color):
        self.image = pg.Surface(size)
        self.rect = pg.Rect(pos, size)
        self.image.fill(color)

    def render(self, surface):
        surface.blit(self.image, self.rect)

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (680, 420)
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock() 

allframes = [
    Frame((10, 10), (50, 50), (0, 255, 0))
]

item_a = allframes[0].rect
tween_a = TweenService.TweenHandler(item_a, TweenService.TweenInfo(), {"left": 100})
tween_a.start()

tween_a.Completed.Connect(lambda *args, **kwargs: allframes[0].image.fill((0, 255, 0)))

running = True 
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT: running = False 
    tween_thread_main.update()
    screen.fill((255, 255, 255))

    for frame in allframes:
        frame.render(screen)

    pg.display.flip()
    clock.tick(60)
