import pygame as pg

pg.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
# image 32pix
TILE = 32

window = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# x y direction offset
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Tank():
    def __init__(self, color, px, py, direct, key_list):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pg.Rect(px, py, TILE, TILE)
        self.direct = direct
####### speed tanks
        self.moves_speed = 4

        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_up = key_list[2]
        self.key_down = key_list[3]
        self.key_shot = key_list[4]

    # movies if button pressed
    def update(self):
        if keys[self.key_left]:
            self.rect.x -= self.moves_speed
            self.direct = 3
        elif keys[self.key_right]:
            self.rect.x += self.moves_speed
            self.direct = 1
        elif keys[self.key_up]:
            self.rect.y -= self.moves_speed
            self.direct = 0
        elif keys[self.key_down]:
            self.rect.y += self.moves_speed
            self.direct = 2

    def draw(self):
        pg.draw.rect(window, self.color, self.rect)
        # direction gun
        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pg.draw.line(window, 'white', self.rect.center, (x, y), 4)


objects = []
# obj - color tank, coordinates, direction, buttons
Tank('green', 100, 275, 0, (pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_SPACE))
Tank('red', 650, 275, 0, (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_KP_ENTER))

play = True
while play:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            play = False

    # traffic control
    keys = pg.key.get_pressed()
    # update obj
    for obj in objects:
        obj.update()

    window.fill('darkgrey')
    for obj in objects:
        obj.draw()

    pg.display.update()
    clock.tick(FPS)

pg.quit()