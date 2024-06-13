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
        self.set_of_environment_low = pygame.sprite.Group()
        self.set_of_environment_mid = pygame.sprite.Group()
        self.set_of_environment_hig = pygame.sprite.Group()
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
        if random.randint(1, 100) == 1 and len(self.set_of_environment) < 40 and (len(self.set_of_environment_low) < 2 or len(self.set_of_environment_mid) < 2 or len(self.set_of_environment_hig) < 2):
            while True:
                coin = random.randint(1,3)
                if coin == 1 and len(self.set_of_environment_low) < 2:
                    y=650
                    break
                elif coin == 2 and len(self.set_of_environment_mid) < 2:
                    y=450
                    break
                elif coin == 3 and len(self.set_of_environment_hig) < 2:
                    y=250
                    break



            start_platform = BasicPlatform(self.image_platform_start, 1400, y)
            if y == 650:
                self.set_of_environment_low.add(start_platform)
            if y == 450:
                self.set_of_environment_mid.add(start_platform)
            if y == 250:
                self.set_of_environment_hig.add(start_platform)


            num_middle_segments = random.randint(1, 2)
            middle_collection = []
            for i in range(num_middle_segments):
                    middle_collection.append(BasicPlatform(self.image_platform_middle,
                                                    1400 + (i+1) * self.image_platform_middle.get_width(), y))


            end_platform = BasicPlatform(self.image_platform_end, 1400 + (
                        num_middle_segments + 1 ) * self.image_platform_middle.get_width(), y)

            self.set_of_environment.add(start_platform)
            for e in middle_collection:
                self.set_of_environment.add(e)
            self.set_of_environment.add(end_platform)

            print(self.set_of_environment_low)


