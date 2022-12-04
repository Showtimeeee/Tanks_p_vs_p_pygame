import pygame as pg
from random import randint

pg.init()

WIDTH, HEIGHT = 900, 600
FPS = 60
# image 32pix
TILE = 40

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('TANKS')
clock = pg.time.Clock()
# font
font_ui = pg.font.Font(None, 42)
# background_image
background_image = pg.image.load('images/greenbg.png').convert()

# x,y direction offset
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Interface:
    def __init__(self):
        pass

    def update(self):
        pass

    # draw health points
    def draw(self):
        pass


class Tank:
    def __init__(self, color, px, py, direct, key_list):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pg.Rect(px, py, TILE, TILE)
        self.direct = direct
        # speed tanks
        self.move_speed = 2
        # health player
        self.hp = 5
        # shot delay
        self.shot_timer = 0
        self.shot_delay = 60
        self.bullet_speed = 5
        self.bullet_damage = 1

        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_up = key_list[2]
        self.key_down = key_list[3]
        self.key_shot = key_list[4]

    # movies if button pressed
    def update(self):
        # old pos if collicion tank
        old_x, old_y = self.rect.topleft
        if keys[self.key_left]:
            self.rect.x -= self.move_speed
            self.direct = 3
        elif keys[self.key_right]:
            self.rect.x += self.move_speed
            self.direct = 1
        elif keys[self.key_up]:
            self.rect.y -= self.move_speed
            self.direct = 0
        elif keys[self.key_down]:
            self.rect.y += self.move_speed
            self.direct = 2

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_x, old_y

        # shooting
        if keys[self.key_shot] and self.shot_timer == 0:
            # speed bullets
            dx = DIRECTS[self.direct][0] * self.bullet_speed
            dy = DIRECTS[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage)
            self.shot_timer = self.shot_delay
        # shot delay(задержка выстрела)
        if self.shot_timer > 0:
            self.shot_timer -= 0.5

    def draw(self):
        pg.draw.rect(window, self.color, self.rect)
        # direction gun
        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pg.draw.line(window, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy
        # if pos bullet
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            # if the bullet exited the screen
            bullets.remove(self)
        else:
            for obj in objects:
                # method checks the collision of the object with the coordinate True
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    # if hits - bullets remove
                    bullets.remove(self)
                    break

    def draw(self):
        pg.draw.circle(window, 'white', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pg.Rect(px, py, size, size)
        # health block
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        pg.draw.rect(window, 'black', self.rect)
        pg.draw.rect(window, 'darkgrey', self.rect, 2)

    def damage(self, value):
        self.hp -= value
        if self.hp <= value:
            objects.remove(self)



bullets = []
# obj - color tank, coordinates, direction, buttons
objects = []
Tank('green', 100, 275, 0, (pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_SPACE))
Tank('red', 650, 275, 0, (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_KP_ENTER))
Ui = Interface()
# block in window
Block(100, 100, TILE)
for b in range(60):
    while True:
        x = randint(0, WIDTH // TILE) * TILE
        y = randint(1, HEIGHT // TILE) * TILE
        rect = pg.Rect(x, y, TILE, TILE)
        finded = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                finded = True

        if not finded:
            break
    Block(x, y, TILE)




play = True
while play:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            play = False
    # traffic control
    keys = pg.key.get_pressed()
    # update obj
    for bullet in bullets:
        bullet.update()
    for obj in objects:
        obj.update()
    Ui.update()

    # window.fill('darkgrey')
    # background
    window.blit(background_image, (0, 0))
    # update obj
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    Ui.draw()

    pg.display.update()
    clock.tick(FPS)

pg.quit()