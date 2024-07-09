import pygame
import sys 
from settings import *
from player import Player

pygame.init()

class Game:
    def __init__(self):
        pygame.init()
        self.displaceSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Western Shooter')
        self.clock = pygame.time.Clock()
        
        #GROUP
        self.allSprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        player = Player((200,200),PATHS['player'],None)
        self.allSprites.add(player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                

            dt = self.clock.tick() / 1000
            
            self.displaceSurface.fill('black')

            self.allSprites.update(dt)
            self.allSprites.draw(self.displaceSurface)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
