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
    def __init__(self,image,x,y,life, level, other_images):
        super().__init__(image,x,y,life)
        self.level = level
        self.right_speed = 0
        self.left_speed = 0
        self.up_speed = 0

        self.right_speed = 0
        self.left_speed = 0
        self.y_speed = 0  # Vertical speed
        self.on_ground = False  # To check if the player is on the ground

        self.frozen = False
        self.starttime = 0

        self.image_basic = image
        self.other_images = other_images


    def move(self,key):
        gravity = 1
        if not self.frozen:
            if key[pygame.K_LEFT]:
                self.rect.x -= 7
            if key[pygame.K_RIGHT]:
                self.rect.x += 7
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
                    if e.type == 1:
                        if not e.flag:
                            e.starttime = pygame.time.get_ticks()
                            ychange = -6
                            e.flag = True

                        if e.flag == True and pygame.time.get_ticks() - e.starttime >= 500:
                            ychange = 6
                            e.flag = False
                            e.kill()

                    if e.type == 2:
                        self.frozen = True
                        self.image = self.other_images[0]
                        self.starttime = pygame.time.get_ticks()



                elif pygame.sprite.collide_rect(self, e) and (self.rect.top < e.rect.bottom):
                    self.rect.top = e.rect.bottom
                    self.y_speed = 0
                elif pygame.sprite.collide_rect(self, e) and (self.rect.left < e.rect.left):
                    self.rect.right = e.rect.left
                    self.y_speed = 0
                elif pygame.sprite.collide_rect(self, e) and (self.rect.left > e.rect.left):
                    self.rect.left = e.rect.right
                    self.y_speed = 0
        else:
            if self.frozen == True and pygame.time.get_ticks() - self.starttime >= 100:
                self.frozen = False
                self.image = self.image_basic









class Environment(Base):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        if self.rect.bottom == 650:
            self.rect.move_ip([-2, 0])
        elif self.rect.bottom == 450:
            self.rect.move_ip([3, 0])
        elif self.rect.bottom == 250:
            self.rect.move_ip([-4, 0])





class BasicPlatform(Environment):
    def __init__(self, image, x, y, type=0):
        super().__init__(image, x, y)
        self.type = type
        self.flag = False
        self.starttime = 0


class Level(Base):
    def __init__(self, image, x, y, surface, image_platform_start, image_platform_middle, image_platform_end, other_platforms):
        super().__init__(image, x, y)
        self.set_of_environment = pygame.sprite.Group()
        self.set_of_environment_low = pygame.sprite.Group()
        self.set_of_environment_mid = pygame.sprite.Group()
        self.set_of_environment_hig = pygame.sprite.Group()
        self.surface = surface

        self.image_platform_start_basic = image_platform_start
        self.image_platform_middle_basic = image_platform_middle
        self.image_platform_end_basic = image_platform_end

        self.image_platform_start = image_platform_start
        self.image_platform_middle = image_platform_middle
        self.image_platform_end = image_platform_end

        self.other_platforms = other_platforms


    def update_level(self):
        self.surface.blit(self.image, (-300, -300))
        self.set_of_environment.update()
        self.set_of_environment.draw(self.surface)

        for e in self.set_of_environment:
            if e.rect.right < 0:
                e.kill()
            if e.rect.right > 1500 and e.rect.bottom == 450:
                e.kill()
            if e.rect.right < 1000:
                if e.rect.bottom == 650:
                    self.set_of_environment_low.remove(e)
                elif e.rect.bottom == 250:
                    self.set_of_environment_hig.remove(e)
            if e.rect.left > 500 and e.rect.bottom == 450:
                self.set_of_environment_mid.remove(e)


    def add_basic_platform(self):
        if random.randint(1, 60) == 1 and len(self.set_of_environment) < 400 and (len(self.set_of_environment_low) < 1 or len(self.set_of_environment_mid) < 1 or len(self.set_of_environment_hig) < 1):
            while True:
                coin = random.randint(1,3)
                if coin == 1 and len(self.set_of_environment_low) < 1:
                    y=650
                    x=1400
                    break
                elif coin == 2 and len(self.set_of_environment_mid) < 1:
                    y=450
                    x=0
                    break
                elif coin == 3 and len(self.set_of_environment_hig) < 1:
                    y=250
                    x=1400
                    break

            coin = random.randint(1, 6)
            if coin == 1:
                type = 1
                self.image_platform_start = self.other_platforms[0]
                self.image_platform_middle = self.other_platforms[1]
                self.image_platform_end = self.other_platforms[2]
            elif coin == 2:
                type = 2
                self.image_platform_start = self.other_platforms[3]
                self.image_platform_middle = self.other_platforms[4]
                self.image_platform_end = self.other_platforms[5]
            else:
                type = 0

            start_platform = BasicPlatform(self.image_platform_start, x, y, type)



            num_middle_segments = random.randint(1, 2)
            middle_collection = []
            for i in range(num_middle_segments):
                    middle_collection.append(BasicPlatform(self.image_platform_middle,
                                                    x + (i+1) * self.image_platform_middle.get_width(), y, type))


            end_platform = BasicPlatform(self.image_platform_end, x + (
                        num_middle_segments + 1 ) * self.image_platform_middle.get_width(), y, type)

            self.set_of_environment.add(start_platform)
            for e in middle_collection:
                self.set_of_environment.add(e)
            self.set_of_environment.add(end_platform)

            if y == 650:
                self.set_of_environment_low.add(end_platform)
            if y == 450:
                self.set_of_environment_mid.add(start_platform)
            if y == 250:
                self.set_of_environment_hig.add(end_platform)

            self.image_platform_start = self.image_platform_start_basic
            self.image_platform_middle = self.image_platform_middle_basic
            self.image_platform_end = self.image_platform_end_basic
