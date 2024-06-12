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
    def __init__(self,image,x,y,life):
        super().__init__(image,x,y)
        self.life = life
