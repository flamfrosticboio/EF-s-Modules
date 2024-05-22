import pygame as pg
import TweenService
from test_classes import LinkedList

tween_thread_main = TweenService.create_main_thread()


class Frame:
    def __init__(self, pos, size, color):
        self.image = pg.Surface(size)
        self.rect = pg.Rect(pos, size)
        self.image.fill(color)

    def render(self, surface):
        image = pg.Surface(self.rect.size)
        image.fill(self.image.get_at((0, 0)))
        surface.blit(image, self.rect)


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (680, 420)
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

allframes = [Frame((10, 10), (50, 50), (255, 0, 0))]

item_a = [200, 200]
tween = TweenService.TweenHandler(
    item_a, TweenService.TweenInfo(), LinkedList(10, 10), use_range = True
)

print(item_a)

tween.start()

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    tween_thread_main.update()
    screen.fill((255, 255, 255))

    allframes[0].rect.topleft = item_a[:2]
    # allframes[0].rect.size = item_a[2]

    # allframes[0].rect.topleft = item_a['my_topleft']
    # allframes[0].rect.size = item_a['my_size']

    for frame in allframes:
        frame.render(screen)

    pg.display.flip()
    clock.tick(60)
