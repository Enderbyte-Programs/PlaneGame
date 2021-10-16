import random
from traceback import format_tb
import pygame
import sys
import os
from tkinter import messagebox, Tk
import datetime
from tkinter import filedialog

def log(message,filename="latest.log"):
    f = open(filename,'a+')
    curtim = str(datetime.datetime.now())
    f.write('['+curtim[0:len(curtim)-3]+']')
    f.write(' '+str(message))
    f.write('\n')
    f.close()

def toplevelerror(message,title='Error'):
    title = str(title)
    message = str(message)
    root = Tk()
    root.wm_attributes("-topmost",True)
    root.withdraw()
    messagebox.showerror(title,message)

def handle_exception(type,value,traceback):
    if issubclass(type, KeyboardInterrupt):
        pass
    else:
        try:
            log('!UNCAUGHT EXCPETION!'+'\n'+str(type)+'\n'+str(value)+'\n'+str(format_tb(traceback)[0]))
        except:
            pass
        toplevelerror('A fatal exception occured. ERROR:\n'+str(type)+'\n'+str(value)+'\n'+str(format_tb(traceback)[0]))
        
        sys.exit()

sys.excepthook = handle_exception
log('Program started')
args = sys.argv
MDECIDER = 0
try:
    fto = args[1]
except:
    log('initializing level')
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("plane.png").convert()
            self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
            self.rect = self.surf.get_rect(center=(500,HEIGHT/2))

        def update(self, pressed_keys):
            if pressed_keys[pygame.K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[pygame.K_DOWN]:
                self.rect.move_ip(0, 5)
            self.rect.move_ip(0,2)

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT

    class Wall(pygame.sprite.Sprite):
        global MDECIDER
        def __init__(self):
            global MDECIDER
            super(Wall,self).__init__()
            self.surf = pygame.Surface((100,random.randint(100,0.75*HEIGHT)))
            self.surf.fill((255,255,255))
            if MDECIDER == 1:
                self.rect = self.surf.get_rect(midtop=((WIDTH-50,0)))
                MDECIDER = 0
            else:
                self.rect = self.surf.get_rect(midbottom=((WIDTH-50,HEIGHT)))
                MDECIDER = 1

        def update(self):
            self.rect.move_ip(-3, 0)
            if self.rect.right < 0:
                self.kill()
            
    pygame.font.init()
    myfont = pygame.font.SysFont('Consolas', 12)
    # Simple pygame program
    if __name__ == "__main__":
        print(__file__)
        PID = os.getpid()
        print(PID)
    # Import and initialize the pygame library
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    print(WIDTH,HEIGHT)
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 5000)
    player = Player()

    all_sprites = pygame.sprite.Group()
    bar = pygame.sprite.Group()
    all_sprites.add(player)
    bg = pygame.image.load("pg_background_1080.png")

    #INSIDE OF THE GAME LOOP
    SCORE = 0
    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()
    tck = 0
    log('started level')
    while running:
        
        # Did the user click the window close button?
        for event in pygame.event.get():
            
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    Tk().withdraw()
                    mln = messagebox.askyesno('PG','Are you sure you want to quit?')
                    if mln == True:
                        running = False
                elif event.key == pygame.K_s:
                    f = open('game.lvl','w+')
                    f.write(str(SCORE)+'\n')
                    f.write(str(player.rect.center))
                    f.close()
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Wall()
                all_sprites.add(new_enemy)
                bar.add(new_enemy)
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        bar.update()

        # Fill the background with white
        screen.fill((0,0,0))
        textsurface = myfont.render('TICK '+str(tck), False, (0, 0, 0))
        textsurface2 = myfont.render('FPS '+str(int(clock.get_fps())), False, (0, 0, 0))
        textsurface3 = myfont.render('TIME '+str(int(pygame.time.get_ticks())), False, (0, 0, 0))
        # Draw a solid blue circle in the center
        screen.blit(bg, (0, 0))
        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)
        # Flip the display
        screen.blit(textsurface,(0,0))
        screen.blit(textsurface2,(100,0))
        screen.blit(textsurface3,(200,0))
        if pygame.sprite.spritecollideany(player, bar):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False
            Tk().withdraw()
            messagebox.showwarning('PG','You Died\nSCORE: '+str(SCORE))
        pygame.display.flip()
        tck += 1
        if tck > 29:
            SCORE += 1
            tck = 0
        clock.tick(60)

    # Done! Time to quit.
    pygame.quit()
    log('saving')
    f = open('game.lvl','w+')
    f.write(str(SCORE)+'\n')
    f.write(str(player.rect.center))
    f.close()
    log('Exiting')