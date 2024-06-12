from asyncio import sleep
import random

import pygame



class Base(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x,y

    def draw(self,surface):
        surface.blit(self.image,self.rect)


class Alive(Base):
    def __init__(self, image, x, y, life):
        super().__init__(image,x,y)
        self.life = life


class Player(Alive):
    def __init__(self,image,x,y,life, level):
        super().__init__(image,x,y,life)
        self.level = level

    def move(self,key):
        self.get_event(key)


        if self.rect.top < 0:
            self.rect.top = 0


    def get_event(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.rect.move_ip([-5, 0])
        if key_pressed[pygame.K_RIGHT]:
            self.rect.move_ip([5, 0])
        if key_pressed[pygame.K_UP] and pygame.sprite.spritecollideany(self, self.level.set_of_environment):
            self.rect.move_ip([0, -100])
        if not key_pressed[pygame.K_RIGHT]:
            self.rect.move_ip([-2, 0])

        if not pygame.sprite.spritecollideany(self, self.level.set_of_environment):
            self.rect.move_ip([0, 3])
      #  if key_pressed[pygame.K_DOWN]:
           # self.rect.move_ip([0, 2])


class Environment(Base):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        self.rect.move_ip([-2, 0])



class BasicPlatform(Environment):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)


class Level(Base):
    def __init__(self, image, x, y, surface, image_platform):
        super().__init__(image, x, y)
        self.set_of_environment = pygame.sprite.Group()
        self.surface = surface
        self.image_platform = image_platform

    def update_level(self):
        self.surface.blit(self.image, (-300, -300))
        self.set_of_environment.update()
        self.set_of_environment.draw(self.surface)

        for e in self.set_of_environment:
            if e.rect.right < 0:
                e.kill()

    def add_basic_platform(self):
        if random.randint(1, 10) == 1 and len(self.set_of_environment) < 10:
            m = BasicPlatform(self.image_platform, random.randint(500, 1300), random.randint(1, 700))
            if not pygame.sprite.spritecollideany(m, self.set_of_environment):
                self.set_of_environment.add(m)

