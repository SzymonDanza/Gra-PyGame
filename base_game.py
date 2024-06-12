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
    def __init__(self,image,x,y,life):
        super().__init__(image,x,y,life)
    def move(self,key):
        self.get_event(key)

    def get_event(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.rect.move_ip([-2, 0])
        if key_pressed[pygame.K_RIGHT]:
            self.rect.move_ip([2, 0])
        if key_pressed[pygame.K_UP]:
            self.rect.move_ip([0, -2])
      #  if key_pressed[pygame.K_DOWN]:
           # self.rect.move_ip([0, 2])

class enviroment(Base):
    def __init__(self,image,x,y):
        super().__init__(image, x, y)
