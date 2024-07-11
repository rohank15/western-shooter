import pygame
import sys
from settings import *  
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite

pygame.init()

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.displaySurf = pygame.display.get_surface()
        self.bg = pygame.image.load('graphics/other/bg.png').convert()
        
    def customDraw(self,player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
        
        self.displaySurf.blit(self.bg,-self.offset)

        for sprite in sorted(self.sprites(), key = lambda sprite : sprite.rect.centery):
            offsetRect = sprite.image.get_rect(center = sprite.rect.center)
            offsetRect.center -= self.offset
            self.displaySurf.blit(sprite.image,offsetRect)   
             
class Game:
    def __init__(self):
        pygame.init()
        self.displaceSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Western Shooter')
        self.clock = pygame.time.Clock()

        #GROUP
        self.allSprites = AllSprites()
        self.setup()

    def setup(self):
        tmxMap = load_pygame('data/map.tmx')
        
        for x,y,surf in tmxMap.get_layer_by_name('Fence').tiles():
            sprite = Sprite((x * 64,y * 64),surf)
            self.allSprites.add(sprite)
        
        self.player = Player((200,200),PATHS['player'],None)
        self.allSprites.add(self.player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


            dt = self.clock.tick(60) / 1000

            self.displaceSurface.fill('black')

            self.allSprites.update(dt)
            self.allSprites.customDraw(self.player)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
