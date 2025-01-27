import pygame
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,path,collisionSprite,createBullet):
        super().__init__()
        
        self.importAssets(path)
        self.frameIndex = 0
        self.status = 'down_idle'

        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(center = pos)

        #MOVEMENT
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 200

        #COLLISION
        self.hitbox = self.rect.inflate(-self.rect.width / 2,-self.rect.height / 2)
        self.collisionSprite = collisionSprite
        
        self.attacking = False
        
        self.createBullet = createBullet
        
        self.bulletShot = False
        self.bulletDirection = pygame.math.Vector2()
        
    def importAssets(self,path):
        self.animations = {}
        
        for index,folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            
            else:
                for fileName in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0] + '/' + fileName
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('/')[2]
                    self.animations[key].append(surf)
                    
    def getStatus(self):
        #IDLE
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        #ATTACKING  
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self,dt):
        currentAnimation = self.animations[self.status]
        
        self.frameIndex += 7 * dt
        
        if int(self.frameIndex) == 2 and self.attacking and not self.bulletShot:
            bulletStartPos = self.rect.center + self.bulletDirection * 50
            self.createBullet(bulletStartPos,self.bulletDirection )
            self.bulletShot = True
            
        if self.frameIndex >= len(currentAnimation):
            self.frameIndex = 0
            if self.attacking:
                self.attacking = False
            
        self.image = currentAnimation[int(self.frameIndex)]         
       
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            #HORIZONTAL MOVEMENT
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'

            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
                
            else:
                self.direction.x = 0
                
            #VERTICAL MOVEMENT
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'

            else:
                self.direction.y = 0
                    
            #ATTACK
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = pygame.math.Vector2(0,0)
                self.frameIndex = 0
                self.bulletShot = False
                
                match self.status.split('_')[0]:
                    case 'left':    self.bulletDirection = pygame.math.Vector2(-1,0)
                    case 'right':    self.bulletDirection = pygame.math.Vector2(1,0)
                    case 'up':    self.bulletDirection = pygame.math.Vector2(0,-1)
                    case 'down':    self.bulletDirection = pygame.math.Vector2(0,1)

    def movement(self,dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #HORIZONTAL MOVEMENT
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x) 
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        #VERTICAL MOVEMENT
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y) 
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self,direction):
        for sprite in self.collisionSprite.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def update(self,dt):
        self.getStatus()
        self.animate(dt)
        self.input()
        self.movement(dt)