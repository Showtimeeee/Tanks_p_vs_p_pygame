import pygame as pg
from random import randint

pg.init()

WIDTH, HEIGHT = 900, 600
FPS = 60
# image 32pix
TILE = 30
#####################
bg_music = pg.mixer.Sound('sounds/engine.mp3')
bg_music.play(loops=-1)

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('TANKS')
clock = pg.time.Clock()
# background_image
background_image = pg.image.load('images/greenbg.png')
# font
font_ui = pg.font.Font(None, 42)
# img bricks
img_brick = pg.image.load('images/block/1.png')
# img_brick = [
#     pg.image.load('images/block/1.png'),
#     pg.image.load('images/block/2.png'),
#     pg.image.load('images/block/3.png')
# ]
# img player
img_tank = [
    pg.image.load('images/z2.png'),
    pg.image.load('images/tank2.png')
]
# img explosion
img_bangs = [
    pg.image.load('images/expl/explosion1.png'),
    pg.image.load('images/expl/explosion2.png'),
    pg.image.load('images/expl/explosion3.png'),
    pg.image.load('images/expl/explosion4.png'),
    pg.image.load('images/expl/explosion5.png'),
    pg.image.load('images/expl/explosion6.png'),
    pg.image.load('images/expl/explosion7.png'),
    pg.image.load('images/expl/explosion8.png'),
    pg.image.load('images/expl/explosion9.png'),
    pg.image.load('images/expl/explosion10.png'),
    pg.image.load('images/expl/explosion11.png'),
    pg.image.load('images/expl/explosion12.png'),
    pg.image.load('images/expl/explosion13.png'),
    pg.image.load('images/expl/explosion14.png'),
    pg.image.load('images/expl/explosion15.png'),
    pg.image.load('images/expl/explosion16.png'),
    pg.image.load('images/expl/explosion17.png'),
    pg.image.load('images/expl/explosion18.png')
]

# x,y direction offset
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Interface:
    def __init__(self):
        pass

    def update(self):
        pass

    # draw health points
    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pg.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                i += 1
                # hp text coordinats in window
                text = font_ui.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1


bang_sound = pg.mixer.Sound('sounds/fire.mp3')


class Tank:
    def __init__(self, color, px, py, direct, key_list):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pg.Rect(px, py, TILE, TILE)
        self.direct = direct
        # speed tanks
        self.move_speed = 3
        # health player
        self.hp = 5
        # shot delay
        self.shot_timer = 2
        self.shot_delay = 40
        self.bullet_speed = 14
        self.bullet_damage = 1

        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_up = key_list[2]
        self.key_down = key_list[3]
        self.key_shot = key_list[4]
        # tank upgrade
        self.rank = 0
        self.image = pg.transform.rotate(img_tank[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    # movies, transorf img
    def update(self):
        self.image = pg.transform.rotate(img_tank[self.rank], -self.direct * 90)
        self.image = pg.transform.scale(self.image, (self.image.get_width() - 5,
                                                     self.image.get_height() -5))
        self.rect = self.image.get_rect(center=self.rect.center)
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
        # tanks block blocks
        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_x, old_y

        # shooting
        if keys[self.key_shot] and self.shot_timer == 0:
            # sound
            self.bang_sound = pg.mixer.Sound('sounds/bullet-ricochet-01.mp3')
            # громкость звука
            self.bang_sound.set_volume(5)
            self.bang_sound.play()
            # speed bullets
            dx = DIRECTS[self.direct][0] * self.bullet_speed
            dy = DIRECTS[self.direct][1] * self.bullet_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bullet_damage)
            self.shot_timer = self.shot_delay
        # shot delay(задержка выстрела)
        if self.shot_timer > 0:
            self.shot_timer -= 0.5

    def draw(self):
        # pg.draw.rect(window, self.color, self.rect)
        # # direction gun
        # x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        # y = self.rect.centery + DIRECTS[self.direct][1] * 30
        # pg.draw.line(window, 'white', self.rect.center, (x, y), 4)
        window.blit(self.image, self.rect)



    def damage(self, value):
        # sound
        self.expl_sound = pg.mixer.Sound('sounds/expl.mp3')
        self.hp -= value
        if self.hp <= 0:

            # громкость звука
            self.expl_sound.set_volume(5)
            self.expl_sound.play()
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

        self.ricocheted_sound = pg.mixer.Sound('sounds/fire.mp3')
        # громкость звука
        self.ricocheted_sound.set_volume(5)


        self.px += self.dx
        self.py += self.dy
        # if pos bullet
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            # if the bullet exited the screen
            bullets.remove(self)

        else:
            for obj in objects:
                # method checks the collision of the object with the coordinate True
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):

                    obj.damage(self.damage)

                    # if hits - bullets remove

                    bullets.remove(self)
                    # boom!
                    Bang(self.px, self.py)
                    self.ricocheted_sound.play()
                    break

    def draw(self):
        pg.draw.circle(window, 'white', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0
        pass

    def update(self):
################# one frame one expl
        self.frame += 0.2
        if self.frame >= 18:
            objects.remove(self)

    def draw(self):
        # animation explosion
        image = img_bangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


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
        window.blit(img_brick, self.rect)
        #pg.draw.rect(window, 'black', self.rect)
        #pg.draw.rect(window, 'darkgrey', self.rect, 2)

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

for b in range(FPS):
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