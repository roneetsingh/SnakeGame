#Imports 
import pygame, sys, random
from pygame import draw
from pygame.math import Vector2

BACKGROUND_COLOR = (110, 110, 5)

class SNAKE:
    def __init__(self):
        self.body=[Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction=Vector2(0,0)
        self.newblock=False

        self.head_up = pygame.image.load('SnakeAppleGraphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('SnakeAppleGraphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('SnakeAppleGraphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('SnakeAppleGraphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('SnakeAppleGraphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('SnakeAppleGraphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('SnakeAppleGraphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('SnakeAppleGraphics/tail_left.png').convert_alpha()
        
        self.body_vertical = pygame.image.load('SnakeAppleGraphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('SnakeAppleGraphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('SnakeAppleGraphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('SnakeAppleGraphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('SnakeAppleGraphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('SnakeAppleGraphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Effects/crunch.wav')
        self.ding_sound = pygame.mixer.Sound('Effects/ding.wav')
        self.crash_sound = pygame.mixer.Sound('Effects/crash.wav')
        self.bg_sound = pygame.mixer.Sound('Effects/bg.wav')

    def draw_snake(self):
        self.updateheadgraphics()
        self.updatetailgraphics()
        for index,block in enumerate(self.body):
            xpos = int(block.x * cellsize)
            ypos = int(block.y * cellsize)
            blockrect = pygame.Rect(xpos,ypos,cellsize,cellsize)
            
            if index == 0:
                gamescreen.blit(self.head,blockrect)
            elif index == len(self.body) - 1:
	            gamescreen.blit(self.tail,blockrect)
            else:
                previousblock = self.body[index + 1] - block
                nextblock = self.body[index - 1] - block
                if previousblock.x == nextblock.x:
                    gamescreen.blit(self.body_vertical,blockrect)
                elif previousblock.y == nextblock.y:
                    gamescreen.blit(self.body_horizontal,blockrect)
                else:
                    if previousblock.x == -1 and nextblock.y == -1 or previousblock.y == -1 and nextblock.x == -1:
                        gamescreen.blit(self.body_tl,blockrect)
                    elif previousblock.x == -1 and nextblock.y == 1 or previousblock.y == 1 and nextblock.x == -1:
                        gamescreen.blit(self.body_bl,blockrect)
                    elif previousblock.x == 1 and nextblock.y == -1 or previousblock.y == -1 and nextblock.x == 1:
                        gamescreen.blit(self.body_tr,blockrect)
                    elif previousblock.x == 1 and nextblock.y == 1 or previousblock.y == 1 and nextblock.x == 1:
                        gamescreen.blit(self.body_br,blockrect)
            

    def updateheadgraphics(self):
        headrelation = self.body[1] - self.body[0]
        if headrelation == Vector2(1,0): 
            self.head = self.head_left
        elif headrelation == Vector2(-1,0): 
            self.head = self.head_right
        elif headrelation == Vector2(0,1): 
            self.head = self.head_up
        elif headrelation == Vector2(0,-1): 
            self.head = self.head_down
    
    def updatetailgraphics(self):
        tailrelation = self.body[-2] - self.body[-1]
        if tailrelation == Vector2(1,0): 
            self.tail = self.tail_left
        elif tailrelation == Vector2(-1,0): 
            self.tail = self.tail_right
        elif tailrelation == Vector2(0,1): 
            self.tail = self.tail_up
        elif tailrelation == Vector2(0,-1):
            self.tail = self.tail_down


    def movesnake(self):
        if self.newblock==True:
            bodycopy=self.body[:]
            bodycopy.insert(0,bodycopy[0]+self.direction)
            self.body=bodycopy[:]
            self.newblock=False
        else:
            bodycopy=self.body[:-1]
            bodycopy.insert(0,bodycopy[0]+self.direction)
            self.body=bodycopy[:]

    def addblock(self):
        self.newblock=True

    def playdingsound(self):
        self.ding_sound.play() 

    def playcrunchsound(self):
        self.crunch_sound.play()

    def playcrashsound(self):
        self.crash_sound.play()

    def playbgsound(self):
        self.bg_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class APPLE:
    def __init__(self):
        self.randomize()

    #draw_apple==draw_fruit
    def draw_apple(self):
        #apple_Rect==fruit_Rect
        apple_rect=pygame.Rect(int(self.position.x*cellsize),int(self.position.y*cellsize),cellsize,cellsize)
        gamescreen.blit(apple,apple_rect)
        #pygame.draw.rect(gamescreen,(126,166,144),apple_rect)

    def randomize(self):
        self.x=random.randint(0,cellnumber-1)
        self.y=random.randint(0,cellnumber-1)
        #position==pos
        self.position=Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake=SNAKE()
        self.apple=APPLE()

    def update(self):
        
        self.snake.movesnake()
        self.collision()
        self.check()

    def drawelements(self):
        self.draw_score()
        self.drawgrass()
        self.apple.draw_apple()
        self.snake.draw_snake()

    def collision(self):
        if self.apple.position== self.snake.body[0]:
            self.apple.randomize()
            self.snake.addblock()
            self.snake.playcrunchsound()

        for block in self.snake.body[1:]:
            if block == self.apple.position:
                self.apple.randomize()

    def check(self):
        if not 0 <= self.snake.body[0].x<cellnumber or not 0 <= self.snake.body[0].y<cellnumber:
            #self.snake.playcrashsound()
            self.gameover()

        for blocks in self.snake.body[1:]:
            if blocks == self.snake.body[0]:
                #self.snake.playcrashsound()
                self.gameover()

    def gameover(self):
        self.snake.reset()

    def drawgrass(self):
        grasscolor = (167,209,61)
        for row in range(cellnumber):
            if row % 2 == 0: 
                for col in range(cellnumber):
                    if col % 2 == 0:
                        grassrect = pygame.Rect(col * cellsize,row * cellsize,cellsize,cellsize)
                        pygame.draw.rect(gamescreen,grasscolor,grassrect)
            else:
                for col in range(cellnumber):
                    if col % 2 != 0:
                        grassrect = pygame.Rect(col * cellsize,row * cellsize,cellsize,cellsize)
                        pygame.draw.rect(gamescreen,grasscolor,grassrect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = font.render(score_text,True,(56,74,12))
        score_x = int(cellsize * cellnumber - 60)
        score_y = int(cellsize * cellnumber - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
        pygame.draw.rect(gamescreen,(167,209,61),bg_rect)

        gamescreen.blit(score_surface,score_rect)
        gamescreen.blit(apple,apple_rect)
        pygame.draw.rect(gamescreen,(56,74,12),bg_rect,2)

    


#Starting entirity of pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

#cellsize==cell_size
#cellnumber==cell_number
cellsize=40
cellnumber=20

#gamescreen==screen
gamescreen=pygame.display.set_mode((cellnumber*cellsize,cellnumber*cellsize))

#Creating clock(gameclock==clock)
gameclock=pygame.time.Clock()
apple=pygame.image.load('SnakeAppleGraphics/apple.png').convert_alpha()
font=pygame.font.Font('Fonts/PoetsenOne-Regular.ttf', 25)
#testsurface(testsurface==test_surface)
#testsurface=pygame.Surface((200,100))
#testsurface.fill((0,0,255))

#testrect==test_rect
#estrect=testsurface.get_rect(center=(320,180))
#xpos=240

#apple=APPLE()
#snake=SNAKE()
SCREENUPDATE=pygame.USEREVENT
pygame.time.set_timer(SCREENUPDATE,150)

maingame=MAIN()


#Starting game loop
while True:
    #maingame.snake.playbgsound()
    #closing game window
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if events.type == SCREENUPDATE:
            maingame.update()
        if events.type == pygame.KEYDOWN:
            if events.key==pygame.K_UP:
                if maingame.snake.direction.y!=1:
                    maingame.snake.direction=Vector2(0,-1)
            if events.key==pygame.K_RIGHT:
                if maingame.snake.direction.x!=-1:
                    maingame.snake.direction=Vector2(1,0)
            if events.key==pygame.K_DOWN:
                if maingame.snake.direction.y!=-1:
                    maingame.snake.direction=Vector2(0,1)
            if events.key==pygame.K_LEFT:
                if maingame.snake.direction.x!=1:
                    maingame.snake.direction=Vector2(-1,0)

        
    
    #filling screen with color
    gamescreen.fill((175,215,70))
    maingame.drawelements()
    #testrect.right+=1
    #pygame.draw.ellipse(gamescreen,pygame.Color('red'),testrect)
    #creating test surface
    #xpos==x_pos
    #xpos+=1
    #gamescreen.blit(testsurface,testrect)

    #Drawing Elements
    pygame.display.update()
    gameclock.tick(60)