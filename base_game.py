from asyncio import sleep
import random

import pygame

YELLOW = pygame.color.THECOLORS['yellow']


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

        self.basic_x = x
        self.basic_y = y
        self.points = 0
        self.points_text = Text(image, x+10, y+10, "0", YELLOW, 50, "Arial")

        self.right_speed = 0
        self.left_speed = 0
        self.y_speed = 0  # Vertical speed
        self.on_ground = False  # To check if the player is on the ground

        self.frozen = False
        self.starttime = 0

        self.slip = False

        self.image_basic = image
        self.other_images = other_images

        self.jump_boost = False
        self.jump_boost_amount = 0
        self.immunity = False
        self.immunity_amount = 0


    def move(self,key):
        gravity = 1
        if not self.frozen:
            if key[pygame.K_LEFT]:
                if self.slip:
                    self.rect.x -= 15
                else:
                    self.rect.x -= 7
            if key[pygame.K_RIGHT]:
                if self.slip:
                    self.rect.x += 15
                else:
                    self.rect.x += 7
            if key[pygame.K_SPACE] and self.on_ground:
                if self.jump_boost:
                    self.y_speed = -30
                    self.jump_boost_amount -= 1
                    if self.jump_boost_amount <= 0:
                        self.jump_boost_amount = 0
                        self.jump_boost = False
                else:
                    self.y_speed = -20 #siła skoku
                if self.immunity:
                    self.immunity_amount -= 1
                    if self.immunity_amount <= 0:
                        self.immunity_amount = 0
                        self.immunity = False
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
                    if e.type == 1 and not self.immunity:
                        if not e.flag:
                            e.starttime = pygame.time.get_ticks()
                            ychange = -6
                            e.flag = True

                        if e.flag == True and pygame.time.get_ticks() - e.starttime >= 500:
                            ychange = 6
                            e.flag = False
                            e.kill()

                    if e.type == 2 and not self.immunity:
                        self.frozen = True
                        self.image = self.other_images[0]
                        self.starttime = pygame.time.get_ticks()

                    if e.type == 3 and not self.immunity:
                        self.slip = True

                    if not e.used_for_points:
                        self.points += 1
                        e.used_for_points = True
                        for h in e.homies:
                            h.used_for_points = True



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

            self.slip = False

        if pygame.sprite.spritecollideany(self, self.level.set_of_powerups):
            for e in self.level.set_of_powerups:
                e.kill()
                if e.type == 1:
                    self.jump_boost = True
                    self.jump_boost_amount += 5

                if e.type == 2:
                    self.immunity = True
                    self.immunity_amount += 7

    def restart_player(self):
        self.immunity_amount = 0
        self.immunity = False
        self.jump_boost_amount = 0
        self.jump_boost = False

        self.right_speed = 0
        self.left_speed = 0
        self.y_speed = 0
        self.on_ground = False

        self.rect.right = self.basic_x
        self.rect.bottom = self.basic_y

        self.points = 0

    def show_points(self):
        self.points_text.text = str(self.points)
        self.points_text.update_text()













class Environment(Base):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.used_for_points = False
        self.homies = []

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


class Powerup(Environment):
    def __init__(self, image, x, y, type=0):
        super().__init__(image, x, y)
        self.type = type
        self.set_of_environment = pygame.sprite.Group()
        self.caught = False

    def update(self, group):
        if not self.caught:
            self.rect.move_ip([0, 3])
        else:
            if self.rect.top < 250:
                self.rect.move_ip([-4, 0])
            elif 250 < self.rect.top < 450:
                self.rect.move_ip([3, 0])
            else:
                self.rect.move_ip([-2, 0])
        self.set_of_environment = group
        if pygame.sprite.spritecollideany(self, self.set_of_environment):
            self.caught = True




class Level(Base):
    def __init__(self, image, x, y, surface, image_platform_start, image_platform_middle, image_platform_end, other_platforms, powerups):
        super().__init__(image, x, y)
        self.set_of_environment = pygame.sprite.Group()
        self.set_of_environment_low = pygame.sprite.Group()
        self.set_of_environment_mid = pygame.sprite.Group()
        self.set_of_environment_hig = pygame.sprite.Group()
        self.set_of_special_platforms = pygame.sprite.Group()
        self.set_of_powerups = pygame.sprite.Group()
        self.surface = surface

        self.image_platform_start_basic = image_platform_start
        self.image_platform_middle_basic = image_platform_middle
        self.image_platform_end_basic = image_platform_end

        self.image_platform_start = image_platform_start
        self.image_platform_middle = image_platform_middle
        self.image_platform_end = image_platform_end

        self.other_platforms = other_platforms
        self.powerups = powerups

    def restart_level(self):
        for e in self.set_of_environment:
            e.kill()
        for e in self.set_of_powerups:
            e.kill()



    def update_level(self):
        self.surface.blit(self.image, (-300, -300))

        self.set_of_powerups.update(self.set_of_environment)
        self.set_of_powerups.draw(self.surface)

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

        for e in self.set_of_powerups:
            if e.rect.top > 740 or e.rect.right < 0 or e.rect.right > 1500:
                e.kill()


    def add_basic_platform(self):
        if random.randint(1, 40) == 1 and len(self.set_of_environment) < 400 and (len(self.set_of_environment_low) < 1 or len(self.set_of_environment_mid) < 1 or len(self.set_of_environment_hig) < 1):
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


            if len(self.set_of_special_platforms) < 2:
                coin = random.randint(1, 12)
            else:
                coin = 12

            if coin <= 3:
                type = 1
                self.image_platform_start = self.other_platforms[0]
                self.image_platform_middle = self.other_platforms[1]
                self.image_platform_end = self.other_platforms[2]
            elif 3 < coin <= 4:
                type = 2
                self.image_platform_start = self.other_platforms[3]
                self.image_platform_middle = self.other_platforms[4]
                self.image_platform_end = self.other_platforms[5]
            elif 4 < coin <= 6:
                type = 3
                self.image_platform_start = self.other_platforms[6]
                self.image_platform_middle = self.other_platforms[7]
                self.image_platform_end = self.other_platforms[8]
            else:
                type = 0

            start_platform = BasicPlatform(self.image_platform_start, x, y, type)
            if coin <= 6:
                self.set_of_special_platforms.add(start_platform)



            num_middle_segments = random.randint(1, 2)
            middle_collection = []
            for i in range(num_middle_segments):
                    middle_collection.append(BasicPlatform(self.image_platform_middle,
                                                    x + (i+1) * self.image_platform_middle.get_width(), y, type))


            end_platform = BasicPlatform(self.image_platform_end, x + (
                        num_middle_segments + 1 ) * self.image_platform_middle.get_width(), y, type)

            homies_list = [start_platform, end_platform]
            for e in middle_collection:
                homies_list.append(e)

            start_platform.homies = homies_list
            end_platform.homies = homies_list
            for e in middle_collection:
                e.homies = homies_list



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

    def add_powerup(self):
       if  random.randint(1, 40) == 1 and len(self.set_of_powerups) < 1:
           if random.randint(1,2) == 1:
               powerup = Powerup(self.powerups[0], random.randint(100, 1300), -100, 1)


           else:
               powerup = Powerup(self.powerups[1], random.randint(100, 1300), -100, 2)

           self.set_of_powerups.add(powerup)
           
    
class Text(Base):
    def __init__(self, image, x, y, text, text_color, font_size, font_type ):
        super().__init__(image, x, y)
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)


    def draw_text(self, surface):
        surface.blit(self.image, self.rect)

    def update_text(self):
        self.image = self.font.render(self.text, True, self.text_color)




class Button(Text):
    def __init__(self, image, x, y, text, text_color, font_size, font_type, background_color, width, height):
        super().__init__(image, x, y, text, text_color, font_size, font_type)
        self.background_color = background_color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y ,self.width, self.height)

    def draw_button(self, surface):
        surface.fill(self.background_color, self.rect)
        self.update_text()
        self.draw_text(surface)
