import pygame as pg
from settings import *
import random

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\sprites\\player.gif")
        self.rect = self.image.get_rect()
        self.vel_x = 0;
        self.vel_y = 0;
        self.can_jump = False
        self.direction = 1
        self.reload_ticks = 0
        self.can_shoot = True
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel_x = - SPEED
            self.direction = -1
        if keys[pg.K_RIGHT]:
            self.vel_x = SPEED
            self.direction = 1
        if keys[pg.K_UP] and self.can_jump:
            self.vel_y -= JUMP
            self.can_jump = False
        if keys[pg.K_x] and self.can_shoot:
            event = pg.event.Event(SHOT_FIRED)
            pg.event.post(event)
            self.reload_ticks = pg.time.get_ticks()
            self.can_shoot = False
        if pg.time.get_ticks() - self.reload_ticks > self.weapon.reload_time:
            self.can_shoot = True
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        self.vel_x = 0
    def draw(self, canvas):
        canvas.blit(self.image, self.rect)

class Block(pg.sprite.Sprite):
    def __init__(self, img_path, x, y, type):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice((True, False))
        if self.type:
            self.image = pg.image.load("img\\sprites\\tree.gif")
            self.image = pg.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            #pg.draw.rect(self.image, (165, 42, 42), self.rect)
            self.hp = 50
            self.speed = 1
        elif not self.type:
            self.image = pg.image.load("img\\sprites\\croc.gif")
            self.image = pg.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect()
            self.hp = 30
            self.speed = 2.5
        self.flaming = False
        #self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 10)
        self.direction = random.choice((-1, 1))
        self.vel_y = 0
    def update(self):
        self.vel_y += GRAVITY
        self.rect.x += self.direction * self.speed
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT:
            self.rect.center = (WIDTH/2, 10)
            if not self.flaming:
                self.flaming = True
                self.speed *=2

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, weapon):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\smallbullet.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = weapon.bullet_speed
        self.damage = weapon.damage
    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

class Weapon:
    def __init__(self, bullet_speed, reload_time, damage, name):
            self.bullet_speed = bullet_speed
            self.reload_time = reload_time
            self.damage = damage
            self.name = name
