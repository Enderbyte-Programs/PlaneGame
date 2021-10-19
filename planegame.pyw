import random
from traceback import format_tb
import pygame
import sys
import os
from tkinter import messagebox, Tk
import datetime

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
        try:
            global STATE
            STATE = "CRASHED"
        except:
            pass
        toplevelerror('A fatal exception occured. ERROR:\n'+str(type)+'\n'+str(value)+'\n'+str(format_tb(traceback)[0]))
        
GAME = "WIN"       

sys.excepthook = handle_exception
log('Program started')
MAINICO = pygame.image.load("ep.ico")
pygame.mixer.init()
pygame.mixer.music.load('pg_music.ogg')
pygame.mixer.music.play(loops=-1)
death_sound = pygame.mixer.Sound('pg_death.ogg')
args = sys.argv
MDECIDER = 0
txl = True
try:
    fto = args[1]
    if not os.path.isfile(fto):
        raise RuntimeError('Invalid file')
except:
    TIME_STARTED = str(datetime.datetime.now())
    log('initializing level')
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("plane.png").convert()
            self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
            self.rect = self.surf.get_rect(center=(500,HEIGHT/2))

        def update(self, pressed_keys):
            global running
            global SCORE
            global GAME
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
                self.kill()
                
                pygame.mixer.music.stop()
                death_sound.play()
                running = False
                GAME = "LOSE"
                toplevelerror('You Died\nSCORE: '+str(SCORE))
            if self.rect.bottom >= HEIGHT:
                self.kill()
                
                
                pygame.mixer.music.stop()
                death_sound.play()
                running = False
                GAME = "LOSE"
                toplevelerror('You Died\nSCORE: '+str(SCORE))
            global ev
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.rect.move_ip(0,-50)

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

    class Button():
        def __init__(self, color, x,y,width,height, text=''):
            self.color = color
            self.ogcol = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self,win,outline=None):
            #Call this method to draw the button on the screen
            if outline:
                pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
                
            pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
            
            if self.text != '':
                font = pygame.font.SysFont('Consolas', 24)
                text = font.render(self.text, 1, (0,0,0))
                win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        def isOver(self, pos):
            global STATE
            #Pos is the mouse position or a tuple of (x,y) coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    self.color = (128,128,128)
                else:
                    self.color = self.ogcol
            else:
                self.color = self.ogcol
            global ev
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[0] > self.x and pos[0] < self.x + self.width:
                        if pos[1] > self.y and pos[1] < self.y + self.height:
                            return True

    # Set up the drawing window
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    print(WIDTH,HEIGHT)
    ADDENEMY = pygame.USEREVENT + 1
    m_ev = pygame.event.Event(ADDENEMY)
    player = Player()

    pygame.display.set_icon(MAINICO)
    pygame.display.set_caption('Plane Game')

    all_sprites = pygame.sprite.Group()
    bar = pygame.sprite.Group()
    all_sprites.add(player)
    bg = pygame.image.load("pg_background_1080.png")
    new_enemy = Wall()
    all_sprites.add(new_enemy)
    bar.add(new_enemy)

    #INSIDE OF THE GAME LOOP
    SCORE = 0
    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()
    tck = 0
    tk = 0
    tick = 0
    log('started level')
    STATE = "RUNNING"
    while running:
        pressed_keys = pygame.key.get_pressed()
        # Did the user click the window close button?
        ev = pygame.event.get()
        for event in ev:
            
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    if STATE == "RUNNING":
                    
                        STATE = "PAUSED"
                        
                        mlx = Button((255,255,0),WIDTH/2,HEIGHT/2,300,20,text='Save and Quit')
                        save = Button((128,255,128),WIDTH/2,HEIGHT/2+100,300,20,text="Save")
                        qt = Button((255,0,0),WIDTH/2-300,HEIGHT/2,300,20,text='Quit without saving')
                        res = Button((0,0,255),WIDTH/2-300,HEIGHT/2+100,300,20,text="Resume")
                    elif STATE == "PAUSED":
                        STATE = "RUNNING"
                    
                    

                
                    
                elif event.key == pygame.K_s:
                    f = open('game.lvl','w+')
                    f.write(str(SCORE)+'\n')
                    f.write(str(player.rect.center)+'\n')
                    f.write(TIME_STARTED)
                    f.close()
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == ADDENEMY and STATE == "RUNNING":
                new_enemy = Wall()
                all_sprites.add(new_enemy)
                bar.add(new_enemy)

            

        if STATE == "RUNNING":
            player.update(pressed_keys)
            bar.update()

        # Fill the background with white
        screen.fill((0,0,0))
        textsurface = myfont.render('TICK '+str(tick), False, (0, 0, 0))
        textsurface2 = myfont.render('FPS '+str(int(clock.get_fps())), False, (0, 0, 0))
        textsurface3 = myfont.render('TIME '+str(int(pygame.time.get_ticks())), False, (0, 0, 0))
        textsurface4 = myfont.render(("STATE "+STATE), False, (0, 0, 0))
        textsurface5 = myfont.render(("SCORE "+str(SCORE)), False, (0, 0, 0))
        textsurface6 = myfont.render(("TIME STARTED "+ TIME_STARTED),False,(0,0,0))
        textsurface7 = myfont.render(("Current Time "+ str(str(datetime.datetime.now())[0:len(str(datetime.datetime.now()))-3])),False,(0,0,0))
        # Draw a solid blue circle in the center
        screen.blit(bg, (0, 0))
        
        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)
        # Flip the display
        screen.blit(textsurface,(0,0))
        screen.blit(textsurface2,(100,0))
        screen.blit(textsurface3,(200,0))
        screen.blit(textsurface4,(300,0))
        screen.blit(textsurface5,(400,0))
        screen.blit(textsurface6,(500,0))
        screen.blit(textsurface7,(900,0))
        if pygame.sprite.spritecollideany(player, bar):
            # If so, then remove the player and stop the loop
            player.kill()
            pygame.mixer.music.stop()
            death_sound.play()
            running = False
            GAME = "LOSE"
            toplevelerror('You Died\nSCORE: '+str(SCORE))

        

        if STATE == "PAUSED":
            qt.draw(screen)
            
            
            if qt.isOver(pygame.mouse.get_pos()) == True:
                
                sys.exit()
            
            
        if STATE == "PAUSED":
            mlx.draw(screen)
            if mlx.isOver(pygame.mouse.get_pos()) == True:
                running = False
        

        if STATE == "PAUSED":
            save.draw(screen)
            if save.isOver(pygame.mouse.get_pos()) == True:
                f = open('game.lvl','w+')
                f.write(str(SCORE)+'\n')
                f.write(str(player.rect.center)+'\n')
                f.write(TIME_STARTED)
                f.close()

        if STATE == "PAUSED":
            res.draw(screen)
            if res.isOver(pygame.mouse.get_pos()) == True:
                STATE = "RUNNING"

            
        tick += 1   
        pygame.display.update()
        if STATE == "RUNNING":
            tck += 1
            tk += 1
            if tk > 250:
                pygame.event.post(m_ev)
                tk = 0
        if tck > 29 and STATE == "RUNNING":
            SCORE += 1
            tck = 0
        clock.tick(60)

    # Done! Time to quit.
    pygame.display.quit()
    if GAME == "WIN":
        log('saving')
        f = open('game.lvl','w+')
        f.write(str(SCORE)+'\n')
        f.write(str(player.rect.center)+'\n')
        f.write(TIME_STARTED)
        f.close()
    else:
        try:
            os.remove('game.lvl')
        except:
            pass
    log('Shutting down sound')
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    log('Exiting')
    sys.exit()



log('reading data')
f = open(fto)
data = f.readlines()
f.close()
try:
    SCORE = int(data[0])
    POSITION = eval(data[1])
    TIME_STARTED = data[2]
    
except:
    try:
        os.remove(fto)
    except:
        pass
    Tk().withdraw()
    messagebox.showerror("Invalid data file.")
class Player(pygame.sprite.Sprite):
    def __init__(self):
        global POSITION
        super(Player, self).__init__()
        self.surf = pygame.image.load("plane.png").convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(center=(int(POSITION[0]),int(POSITION[1])))

    def update(self, pressed_keys):
        global running
        global SCORE
        global GAME
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
            self.kill()
            
            pygame.mixer.music.stop()
            death_sound.play()
            running = False
            GAME = "LOSE"
            toplevelerror('You Died\nSCORE: '+str(SCORE))
        if self.rect.bottom >= HEIGHT:
            self.kill()
            
            
            pygame.mixer.music.stop()
            death_sound.play()
            running = False
            GAME = "LOSE"
            toplevelerror('You Died\nSCORE: '+str(SCORE))
        global ev
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.rect.move_ip(0,-50)

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

class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.ogcol = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('Consolas', 24)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        global STATE
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = (128,128,128)
            else:
                self.color = self.ogcol
        else:
            self.color = self.ogcol
        global ev
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > self.x and pos[0] < self.x + self.width:
                    if pos[1] > self.y and pos[1] < self.y + self.height:
                        return True

# Set up the drawing window
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
print(WIDTH,HEIGHT)
ADDENEMY = pygame.USEREVENT + 1
m_ev = pygame.event.Event(ADDENEMY)
player = Player()

pygame.display.set_icon(MAINICO)
pygame.display.set_caption("Plane Game")

all_sprites = pygame.sprite.Group()
bar = pygame.sprite.Group()
all_sprites.add(player)
bg = pygame.image.load("pg_background_1080.png")
new_enemy = Wall()
all_sprites.add(new_enemy)
bar.add(new_enemy)

#INSIDE OF THE GAME LOOP
# Run until the user asks to quit
running = True
clock = pygame.time.Clock()
tck = 0
tk = 0
tick = 0
log('started level')
STATE = "RUNNING"
while running:
    pressed_keys = pygame.key.get_pressed()
    # Did the user click the window close button?
    ev = pygame.event.get()
    for event in ev:
        
        # Did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == pygame.K_ESCAPE:
                if STATE == "RUNNING":
                
                    STATE = "PAUSED"
                    
                    mlx = Button((255,255,0),WIDTH/2,HEIGHT/2,300,20,text='Save and Quit')
                    save = Button((128,255,128),WIDTH/2,HEIGHT/2+100,300,20,text="Save")
                    qt = Button((255,0,0),WIDTH/2-300,HEIGHT/2,300,20,text='Quit without saving')
                    res = Button((0,0,255),WIDTH/2-300,HEIGHT/2+100,300,20,text="Resume")
                elif STATE == "PAUSED":
                    STATE = "RUNNING"
                
                

            
                
            elif event.key == pygame.K_s:
                f = open('game.lvl','w+')
                f.write(str(SCORE)+'\n')
                f.write(str(player.rect.center)+'\n')
                f.write(TIME_STARTED)
                f.close()
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY and STATE == "RUNNING":
            new_enemy = Wall()
            all_sprites.add(new_enemy)
            bar.add(new_enemy)

        

    if STATE == "RUNNING":
        player.update(pressed_keys)
        bar.update()

    # Fill the background with white
    screen.fill((0,0,0))
    textsurface = myfont.render('TICK '+str(tick), False, (0, 0, 0))
    textsurface2 = myfont.render('FPS '+str(int(clock.get_fps())), False, (0, 0, 0))
    textsurface3 = myfont.render('TIME '+str(int(pygame.time.get_ticks())), False, (0, 0, 0))
    textsurface4 = myfont.render(("STATE "+STATE), False, (0, 0, 0))
    textsurface5 = myfont.render(("SCORE "+str(SCORE)), False, (0, 0, 0))
    textsurface6 = myfont.render(("TIME STARTED "+ TIME_STARTED),False,(0,0,0))
    textsurface7 = myfont.render(("Current Time "+ str(str(datetime.datetime.now())[0:len(str(datetime.datetime.now()))-3])),False,(0,0,0))
    # Draw a solid blue circle in the center
    screen.blit(bg, (0, 0))
    
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    # Flip the display
    screen.blit(textsurface,(0,0))
    screen.blit(textsurface2,(100,0))
    screen.blit(textsurface3,(200,0))
    screen.blit(textsurface4,(300,0))
    screen.blit(textsurface5,(400,0))
    screen.blit(textsurface6,(500,0))
    screen.blit(textsurface7,(900,0))
    if pygame.sprite.spritecollideany(player, bar):
        # If so, then remove the player and stop the loop
        player.kill()
        pygame.mixer.music.stop()
        death_sound.play()
        running = False
        GAME = "LOSE"
        toplevelerror('You Died\nSCORE: '+str(SCORE))

    

    if STATE == "PAUSED":
        qt.draw(screen)
        
        
        if qt.isOver(pygame.mouse.get_pos()) == True:
            
            sys.exit()
        
        
    if STATE == "PAUSED":
        mlx.draw(screen)
        if mlx.isOver(pygame.mouse.get_pos()) == True:
            running = False
    

    if STATE == "PAUSED":
        save.draw(screen)
        if save.isOver(pygame.mouse.get_pos()) == True:
            f = open('game.lvl','w+')
            f.write(str(SCORE)+'\n')
            f.write(str(player.rect.center)+'\n')
            f.write(TIME_STARTED)
            f.close()

    if STATE == "PAUSED":
        res.draw(screen)
        if res.isOver(pygame.mouse.get_pos()) == True:
            STATE = "RUNNING"

        
    tick += 1   
    pygame.display.update()
    if STATE == "RUNNING":
        tck += 1
        tk += 1
        if tk > 250:
            pygame.event.post(m_ev)
            tk = 0
    if tck > 29 and STATE == "RUNNING":
        SCORE += 1
        tck = 0
    clock.tick(60)

# Done! Time to quit.
pygame.display.quit()
if GAME == "WIN":
    log('saving')
    f = open('game.lvl','w+')
    f.write(str(SCORE)+'\n')
    f.write(str(player.rect.center)+'\n')
    f.write(TIME_STARTED)
    f.close()
else:
    try:
        os.remove('game.lvl')
    except:
        pass
log('Shutting down sound')
pygame.mixer.music.stop()
pygame.mixer.quit()
log('Exiting')
sys.exit()