#initialize the screen
import pygame, math, sys
from pygame.locals import *
import time
import os

def car_game(func):
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    #GAME CLOCK
    clock = pygame.time.Clock()
    font = pygame.font.Font('simhei.ttf', 20)
    running = True
    win_text = font.render('', True, (0, 255, 0))
    
    def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
    
    class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location
    
    class CarSprite(pygame.sprite.Sprite):
        def __init__(self, image, x, y):            
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.image_orig = self.image
            self.screen = pygame.display.get_surface()
            self.area = self.screen.get_rect()
            self.x = x
            self.y = y
            self.rect.topleft = self.x, self.y
            #self.x, self.y = findspawn()
            self.dir = 0
            self.speed = 0.0
            self.maxspeed = 11.5
            self.minspeed = -1.85
            self.acceleration = 0.095
            self.deacceleration = 0.12
            self.softening = 0.04
            self.steering = 1.60
        
        def update(self, deltat):
            self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
            self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        
        def impact(self):
            if self.speed > 0:
                self.speed = self.minspeed

        def soften(self):
            if self.speed > 0:
                self.speed -= self.softening
            if self.speed < 0:
                self.speed += self.softening

    #Accelerate the vehicle
        def accelerate(self):
            if self.speed < self.maxspeed:
                self.speed = self.speed + self.acceleration

    #Deaccelerate.
        def deaccelerate(self):
            if self.speed > self.minspeed:
                self.speed = self.speed - self.deacceleration

    #Steer.
        def steerleft(self):
            self.dir = self.dir+self.steering
            if self.dir > 360:
                self.dir = 0
            self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

    #Steer.
        def steerright(self):
            self.dir = self.dir-self.steering
            if self.dir < 0:
                self.dir = 360  
            self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        
    class PadSprite(pygame.sprite.Sprite):
        normal = pygame.image.load('blank.png')
        def __init__(self, x, y):
            super(PadSprite, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = (x, y)
            self.image = self.normal
            self.rect.x = x
            self.rect.y = y
        def update(self):
            self.image = self.normal
    
    pads = [
        PadSprite(500, 20),
        PadSprite(500, 450)
    ]
    pad_group = pygame.sprite.RenderPlain(*pads)
    
    # Create Target Sprite
    class TargetSprite(pygame.sprite.Sprite):
        normal = pygame.image.load('target1.png')
        def __init__(self, x, y):
            super(TargetSprite, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = (x, y)
            self.image = self.normal
            self.rect.x = x
            self.rect.y = y
        def update(self):
            self.image = self.normal
    

    # CREATE A CAR AND RUN
    rect = screen.get_rect()
    car = CarSprite('car_1.png', 400, 100)
    car_group = pygame.sprite.RenderPlain(car)
    BackGround = Background('NEAREST.jpg', [0,0])
    
    # create target for ending
    target = TargetSprite(490, 380)
    target_group = pygame.sprite.RenderPlain(target)
    
    # GET START TIME
    start_time = time.time()
    flag = True

    #THE GAME LOOP
    while running:
        #USER INPUT

        deltat = clock.tick(60)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            if event.key == K_ESCAPE: 
                pygame.quit()
                running = False
                os._exit(00)
 
        if running:
            # This is about keyboard!
            keys = pygame.key.get_pressed()                
            if keys[K_LEFT]:
                car.steerleft()
            if keys[K_RIGHT]:
                car.steerright()
            if keys[K_UP]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_DOWN]:
                car.deaccelerate()
                
            x = car.x
            y = car.y
            ## your code here!!
            
            exec(func(x,y))
            
            
            #RENDERING
            #screen.fill((0,0,0))
            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            text_x = '小车的横向位置: {:.3f}'.format(car.x)
            text_y = '小车的纵轴位置: {:.3f}'.format(car.y)
            win_text_x = font.render(text_x, True, (0, 255, 0))
            win_text_y = font.render(text_y, True, (0, 255, 0))
            
            # GET END_TIME
            if flag:
                end_time = time.time()
            time_range = "停车所需时间: {:.2f}".format(end_time - start_time)
            time_text = font.render(time_range, True, (0, 255, 0))
            
            
            for pad in pads:
                if car.rect.colliderect(pad.rect):
                    hint_text = font.render("撞毁! 按空格键重启游戏!", True, (255,0,0))
                    screen.blit(hint_text, (300, 300))
                    car.kill()
            
            if car.rect.collidepoint(target.rect.center):
                hint_text = font.render("抵达终点! 按空格键重启游戏!", True, (255,0,0))
                screen.blit(hint_text, (280, 280))
                hint_text = font.render("你本次所用的时间为："+time_range, True, (255,0,0))
                screen.blit(hint_text, (280, 300))
                hint_text = font.render("你本次名次为："+str(num), True, (255,0,0))
                screen.blit(hint_text, (280, 320))
                car.kill()
                flag = False
                    
            if keys[K_SPACE]:
                car = CarSprite('car_1.png', 400, 100)
                start_time = time.time()
                car_group = pygame.sprite.RenderPlain(car)
                hint_text = font.render("", True, (255,0,0))
                screen.blit(hint_text, (300, 300))
                flag = True
            
            car_group.update(deltat)
            car_group.draw(screen)
            #screen.blit(car.image, car.rect)
            pad_group.draw(screen)
            target_group.draw(screen)
            #pygame.draw.rect(screen,(255, 200, 0), car.rect)
            screen.blit(win_text_x, (50, 50))
            screen.blit(win_text_y, (50, 70))
            screen.blit(time_text, (50, 90))

            #Counter Render
            pygame.display.flip()
