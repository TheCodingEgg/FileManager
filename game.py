from math import sqrt
import random

import pygame
from pygame.locals import (K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_a, K_d,
                           K_s, K_w)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    speed = 6
    health = 0
    pos = [0, 0]
    immune = False
    old_direction = 0

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.image = pygame.image.load(".\\Assets\\player.png").convert()
        self.rect = self.image.get_rect()
        self.pos = [(SCREEN_WIDTH - self.rect.width)/2,
                    (SCREEN_HEIGHT - self.rect.height)/2]
        self.health = 150

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.pos[1] -= self.speed
            if self.pos[1] < self.rect.height/2:
                self.pos[1] = self.rect.height/2
            self.heading(0)
        if pressed_keys[K_s]:
            self.pos[1] += self.speed
            if self.pos[1] > SCREEN_HEIGHT - self.rect.height/2:
                self.pos[1] = SCREEN_HEIGHT - self.rect.height/2
            self.heading(2)
        if pressed_keys[K_a]:
            self.pos[0] -= self.speed
            if self.pos[0] < self.rect.width/2:
                self.pos[0] = self.rect.width/2
            self.heading(1)
        if pressed_keys[K_d]:
            self.pos[0] += self.speed
            if self.pos[0] > SCREEN_WIDTH - self.rect.width/2:
                self.pos[0] = SCREEN_WIDTH - self.rect.width/2
            self.heading(3)
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])

    def heading(self, direction):
        self.image = pygame.transform.rotate(
            self.image, (direction - self.old_direction) * 90)
        self.old_direction = direction

    def trajectory(self, ms_pos):
        speed = 5
        if ms_pos[0] > self.pos[0]:
            speed *= 1
        else:
            speed *= -1
        m = (float(ms_pos[1]) - float(self.pos[1])) / \
            (float(ms_pos[0]) - float(self.pos[0]))
        v2 = m * speed
        return [speed, v2]


class Projectile(pygame.sprite.Sprite):
    pos = []
    speed = []

    def __init__(self, player, speed):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface((5, 5))
        self.image = pygame.image.load(".\\Assets\\bullet.png").convert()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.pos = [player.rect.centerx, player.rect.centery]

    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])


class Enemy(pygame.sprite.Sprite):
    speed = 0
    pos = [0, 0]

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.image = pygame.image.load(".\\Assets\\asteroid.png").convert()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.pos = [random.randrange(
            0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT)]

    def find_path(self, player):
        if player.rect.centerx > self.rect.centerx:
            self.pos[0] += self.speed
        if player.rect.centerx < self.rect.centerx:
            self.pos[0] -= self.speed
        if player.rect.centery > self.rect.centery:
            self.pos[1] += self.speed
        if player.rect.centery < self.rect.centery:
            self.pos[1] -= self.speed
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])

    def killEnemy(self, ms_pos, enemies):
        rect2 = pygame.Rect(0, 0, 75, 75)
        rect2.center = ms_pos
        if rect2.colliderect(self):
            enemies.remove(self)


def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player()
    bullets = []
    enemies = []
    running = True
    ms_pos = (-1, -1)
    time = 0
    difficulty = 64
    clock = pygame.time.Clock()

    bkgd = pygame.image.load(".\\Assets\\background.jpg")

    font = pygame.font.SysFont(None, 40)
    img = font.render(str(player.health), True, (0, 255, 0))

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                ms_pos = pygame.mouse.get_pos()
                bullets.append(Projectile(player, player.trajectory(ms_pos)))
            elif event.type == QUIT:
                running = False

        screen.blit(bkgd, (0, 0))
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        screen.blit(player.image, player.rect)
        for enemy in enemies:
            enemy.find_path(player)
            screen.blit(enemy.image, enemy.rect)
            if enemy.rect.colliderect(player) and player.immune == False:
                player.health -= 50
                player.immune = True
                time = pygame.time.get_ticks()
                print(player.health, time, player.immune)
                if player.health <= 0:
                    running = False

        if(pygame.time.get_ticks() - time > 512):
            player.immune = False

        if(pygame.time.get_ticks() - time > 4096 and player.health < 150):
            player.health += 50
            if player.health > 150:
                player.health = 150

        for bullet in bullets:
            bullet.update()
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.collidelist(enemies) != -1:
                enemies.remove(enemies[bullet.rect.collidelist(enemies)])
                bullets.remove(bullet)
            if screen.get_rect().contains(bullet.rect) == False:
                bullets.remove(bullet)

        if pygame.time.get_ticks() % difficulty == 0:
            x = Enemy()
            enemies.append(x)
            dist = sqrt((player.pos[0] - x.pos[0]) * (player.pos[0] - x.pos[0]) +
                        (player.pos[1] - x.pos[1]) * (player.pos[1] - x.pos[1]))
            # print(dist)
            if dist < SCREEN_WIDTH/6:
                enemies.remove(x)
        img = font.render(str(player.health), True, (0, 255, 0))
        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    print("Your score is", pygame.time.get_ticks())


if __name__ == '__main__':
    game()
