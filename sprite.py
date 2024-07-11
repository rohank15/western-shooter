import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-self.rect.height / 3)