from asyncio import sleep
import random

import pygame



class Base(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.bottom = y

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
        self.right_speed = 0
        self.left_speed = 0
        self.up_speed = 0

        self.right_speed = 0
        self.left_speed = 0
        self.y_speed = 0  # Vertical speed
        self.on_ground = False  # To check if the player is on the ground


    def move(self,key):
        gravity = 1

        if key[pygame.K_LEFT]:
            self.rect.x -= 5
        if key[pygame.K_RIGHT]:
            self.rect.x += 5
        if key[pygame.K_SPACE] and self.on_ground:
            self.y_speed = -20  # Adjust this value for jump strength
            self.on_ground = False

        # Apply gravity
        self.y_speed += gravity
        self.rect.y += self.y_speed

        # Check if player is on the ground
        if self.rect.bottom >= 740:
            self.rect.bottom = 740
            self.y_speed = 0
            self.on_ground = True

        if pygame.sprite.spritecollideany(self, self.level.set_of_environment):
            for e in self.level.set_of_environment:
                if pygame.sprite.collide_rect(self, e) and (self.rect.bottom > e.rect.top) and (self.rect.top < e.rect.top) and (self.rect.top < e.rect.bottom):
                    self.rect.bottom = e.rect.top
                    self.y_speed = 0
                    self.on_ground = True
                elif pygame.sprite.collide_rect(self, e) and (self.rect.top < e.rect.bottom):
                    self.rect.top = e.rect.bottom
                    self.y_speed = 0
                elif pygame.sprite.collide_rect(self, e) and (self.rect.left < e.rect.left):
                    self.rect.right = e.rect.left
                    self.y_speed = 0
                elif pygame.sprite.collide_rect(self, e) and (self.rect.left > e.rect.left):
                    self.rect.left = e.rect.right
                    self.y_speed = 0






class Environment(Base):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        self.rect.move_ip([-2, 0])



class BasicPlatform(Environment):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)


class Level(Base):
    def __init__(self, image, x, y, surface, image_platform_start, image_platform_middle, image_platform_end):
        super().__init__(image, x, y)
        self.set_of_environment = pygame.sprite.Group()
        self.surface = surface
        self.image_platform_start = image_platform_start
        self.image_platform_middle = image_platform_middle
        self.image_platform_end = image_platform_end


    def update_level(self):
        self.surface.blit(self.image, (-300, -300))
        self.set_of_environment.update()
        self.set_of_environment.draw(self.surface)

        for e in self.set_of_environment:
            if e.rect.right < 0:
                e.kill()

    def add_basic_platform(self):
        if random.randint(1, 100) == 1 and len(self.set_of_environment) < 40:
            coin = random.randint(1,3)
            if coin == 1:
                y=650
            elif coin == 2:
                y=450
            elif coin == 3:
                y=250



            start_platform = BasicPlatform(self.image_platform_start, 1400, y)


            num_middle_segments = random.randint(1, 3)
            print(num_middle_segments)
            for i in range(num_middle_segments):

                middle_platform = BasicPlatform(self.image_platform_middle,
                                                    1400 + i * self.image_platform_middle.get_width(), y)


            end_platform = BasicPlatform(self.image_platform_end, 1400 + (
                        num_middle_segments ) * self.image_platform_middle.get_width(), y)

            self.set_of_environment.add(start_platform)
            self.set_of_environment.add(middle_platform)
            self.set_of_environment.add(end_platform)


