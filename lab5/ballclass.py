import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
speedrange = 4  #speed range of the balls and squares 
ballscore = 1  #points for a ball 
squarescore = 2  #points for a square 
score = 0
lifespan = 60
balls = []
squares = []
screen = pygame.display.set_mode((800, 600))

leaderboard = {}
leaderboardfile = open('leaderboard.txt')
leaders = leaderboardfile.readlines()
for i in range(len(leaders)):
    leaderboard[leaders[i].rstrip().split('\t')[0]] = leaders[i].rstrip().split('\t')[1]
    leaders[i] = leaders[i].rstrip().split('\t')[0]
leaderboardfile.close()

while len(leaders) < 3:
    leaders.append('empty')
leaderboard['empty'] = '0'

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class Ball:
    '''
    x, y - coordinates of the ball
    vx, vy - speed of the ball
    r - radius of the ball
    i - number of the ball's color in COLOR
    life - amount of tics ball have left to live
    '''
    
    def __init__(self, xborder, yborder, speedrange, lifespan, rmax, balls):
        '''
        function generates a ball
        takes (xborder, yborder, speedrange, lifespan, rmax)
        xborder - tuple (left x border, right x border)
        yborder - tuple (top y border, bottom y border)
        speedrange - max speed of the ball
        lifespan - max life of the ball
        rmax - max radius of the ball
        balls - list of already existing balls
        all parameters are randomized
        '''
        colliding = True
        while colliding:
            self.r = randint(rmax//2,rmax)
            self.x = randint(xborder[0] + speedrange + self.r,
                xborder[1] - speedrange - self.r)
            self.y = randint(yborder[0] + speedrange + self.r,
                yborder[1] - speedrange - self.r)
            colliding = False
            for ball in balls:
                if  (ball.x - self.x) * (ball.x - self.x )+ \
                        (ball.y - self.y) * (ball.y - self.y) < \
                        (ball.r + self.r) * (ball.r + self.r):
                    colliding = True
        self.vx = randint (-speedrange, speedrange)
        self.vy = randint (-speedrange, speedrange)
        self.i = randint(0, 5)
        self.life = randint(lifespan//2, lifespan)
    
    
    def move(self, xborder, yborder):
        '''
        function moves a ball and does collisions with borders
        takes (xborder, yborder)
        xborder - tuple (left x border, right x border)
        yborder - tuple (top y border, bottom y border)
        '''
        self.x += self.vx
        self.y += self.vy
        if self.x < (xborder[0] + self.r):
            self.vx = - self.vx
            self.x = (xborder[0] + self.r)
        if self.x > (xborder[1] - self.r):
            self.vx = - self.vx
            self.x = (xborder[1] - self.r)
        if self.y < (yborder[0] + self.r):
            self.vy = - self.vy
            self.y = (yborder[0] + self.r)
        if self.y > (yborder[1] - self.r):
            self.vy = - self.vy
            self.y = (yborder[1] - self.r)
        self.life += -1
    
    
    def draw(self):
        '''
        function draws a ball
        '''
        circle(screen, COLOR[self.i], (self.x, self.y), self.r)
    
    
    def clicked(self, event):
        '''
        function checks if the ball was clicked
        takes a click event
        returns a bull - "Was the ball clicked?"
        '''
        xmouse, ymouse = event.pos
        clicked = (xmouse - self.x) * (xmouse - self.x) + (ymouse\
            - self.y) * (ymouse-self.y) < self.r * self.r
        return(clicked)


class Square:
    '''
    x, y - coordinates of the left top corner of the square
    vx, vy - base speed of the square (square gets faster)
    a - size of the square
    i - number of the square's color in COLOR
    life - amount of tics square have left to live
    live - amout of tics square had left to live when created
    '''
    
    def __init__(self, xborder, yborder, speedrange, lifespan, amax, squares):
        '''
        function generates a square
        takes (xborder, yborder, speedrange, lifespan, amax)
        xborder - tuple (left x border, right x border)
        yborder - tuple (top y border, bottom y border)
        speedrange - max speed of the square
        lifespan - max life of the square
        amax - max size of the square
        squares - list of already existing squares
        all parameters are randomized
        '''
        colliding = True
        while colliding:
            self.a = randint(amax // 2 , amax)
            self.x = randint(xborder[0] + speedrange,
                xborder[1] - speedrange - self.a)
            self.y = randint(yborder[0] + speedrange,
                yborder[1] - speedrange - self.a)
            colliding = False
            for square in squares:
                if  ((square.y - self.y) > 0 and (square.y - self.y)\
                        < self.a) or ((square.y - self.y) < 0 and (square.y\
                        - self.y) > - square.a) or ((square.x - self.x) > 0\
                        and (square.x - self.x) < self.a) or ((square.x -\
                        self.x) < 0 and (square.x - self.x) > - square.a):
                    colliding = True
        self.vx = randint (-speedrange, speedrange)
        self.vy = randint (-speedrange, speedrange)
        self.i = randint(0, 5)
        self.life = randint(lifespan // 2, lifespan)
        self.live = self.life
    
    
    def move(self, xborder, yborder):
        '''
        function moves a square and does collisions with borders
        takes (xborder, yborder)
        xborder - tuple (left x border, right x border)
        yborder - tuple (top y border, bottom y border)
        '''
        self.x += int(self.vx * (2 - self.life/self.live))
        self.y += int(self.vy * (2 - self.life/self.live))
        if self.x < (xborder[0]):
            self.vx = - self.vx
            self.x = (xborder[0])
        if self.x > (xborder[1] - self.a):
            self.vx = - self.vx
            self.x = (xborder[1] - self.a)
        if self.y < (yborder[0]):
            self.vy = - self.vy 
            self.y = (yborder[0])
        if self.y > (yborder[1] - self.a):
            self.vy = - self.vy
            self.y = (yborder[1] - self.a)
        self.life += -1
    
    
    def draw(self):
        '''
        function draws a square
        '''
        rect(screen, COLOR[self.i], (self.x, self.y, self.a, self.a))
    
    
    def clicked(self, event):
        '''
        function checks if the square was clicked
        takes a click event
        returns a bull - "Was the square clicked?"
        '''
        xmouse, ymouse = event.pos
        clicked = xmouse > self.x and xmouse < (self.x+self.a)\
            and ymouse > self.y and ymouse < (self.y+self.a)
        self.vy = - self.vy
        self.vx = - self.vx
        return(clicked)


def drawleaders(leaders, leaderboard):
    '''
    function draw a leaderboard in the corner
    takes a list of leaders' names as str from best to worst and
        a dictionary with names as str as keys and scores as values as str
    '''
    screen.blit(pygame.font.Font(None, 20).render(leaders[0], 1, BLACK), (500, 510))
    screen.blit(pygame.font.Font(None, 20).render(leaderboard[leaders[0]], 1, BLACK), (600, 510))
    screen.blit(pygame.font.Font(None, 20).render(leaders[1], 1, BLACK), (500, 540))
    screen.blit(pygame.font.Font(None, 20).render(leaderboard[leaders[1]], 1, BLACK), (600, 540))
    screen.blit(pygame.font.Font(None, 20).render(leaders[2], 1, BLACK), (500, 570))
    screen.blit(pygame.font.Font(None, 20).render(leaderboard[leaders[2]], 1, BLACK), (600, 570))


def work(objects):
    '''
    function takes a list of balls or squares
    deletes ones that lived too long
    moves and draws others
    returns a list of objects after moving and deleting
    '''
    k = 0
    for i in range(len(objects)):
        if objects[i-k].life < 0:
            objects.pop(i-k)
            k += 1
        else:
            objects[i-k].move((100, 700), (100, 500))
            objects[i-k].draw()
    return(objects)


def ballcoli(balls): 
    '''
    checks for collisions between balls
    takes a list of balls
    reverses speeds of colliding balls
    returns new list of balls
    '''
    for i in range(len(balls)):
        for m in range(len(balls)-i):
            if (balls[i].x - balls[i+m].x)*(balls[i].x - balls[i+m].x)+\
                    (balls[i].y - balls[i+m].y)*(balls[i].y - balls[i+m].y) <\
                    (balls[i].r + balls[i+m].r)*(balls[i].r + balls[i+m].r):
                balls[i].vx = - balls[i].vx
                balls[i].vy = - balls[i].vy
                balls[i+m].vx = - balls[i+m].vx
                balls[i+m].vy = - balls[i+m].vy
    return(balls)


def squarecoli(squares): 
    '''
    checks for collisions between squares
    takes a list of squares
    reverses speeds of colliding squares
    returns new list of squares
    '''
    for i in range(len(squares)):
        for m in range(len(squares)-i):
            if squares[i].x + squares[i].a > squares[i+m].x and squares[i+m].x +\
                    squares[i+m].a > squares[i].x and squares[i].y + squares[i].a >\
                    squares[i+m].y and squares[i+m].y + squares[i+m].a > squares[i].y:
                squares[i].vx = - squares[i].vx 
                squares[i+m].vx = - squares[i+m].vx
                squares[i].vy = - squares[i].vy
                squares[i+m].vy = - squares[i+m].vy
    return(squares)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished: #gameplay
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            k = 0
            m = 0
            for i in range(len(balls)):
                if balls[i-k].clicked(event):
                    balls.pop(i-k)
                    k += 1
            for i in range(len(squares)):
                if squares[i-m].clicked(event):
                    squares.pop(i-m)
                    m += 1
            score += ballscore*k + squarescore*m
    if len(balls) < 6:
        balls.append(Ball((100, 700), (100, 500), speedrange, lifespan, 50, balls))
    if len(squares) < 6:
        squares.append(Square((100, 700), (100, 500), speedrange, lifespan, 100, squares))
    balls = work(balls)
    balls = ballcoli(balls)
    squares = work(squares)
    squares = squarecoli(squares)
    screen.blit(pygame.font.Font(None, 60).render(str(score), 1, BLACK), (20, 20))
    drawleaders(leaders, leaderboard)
    pygame.display.update()
    screen.fill(WHITE)
    rect(screen, BLACK, (100,100, 600, 400))

done = False
name = ''

while not done: #name enter screen
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                done = True
            else:
                name += event.unicode
        if event.type == pygame.QUIT:
            done = True
    if len(name) > 6:
        done = True
    screen.blit(pygame.font.Font(None, 60).render("YOUR NAME?", 1, WHITE), (200, 200))
    screen.blit(pygame.font.Font(None, 60).render(name, 1, WHITE), (200, 300))
    pygame.display.update()
    screen.fill(WHITE)
    rect(screen, BLACK, (100,100, 600, 400))

if len(name) > 0:
    place=0
    if name in leaders:
        if score > int(leaderboard[name]):
            leaderboard[name] = score
    else:
        for i in range(len(leaders)):
            if score <= int(leaderboard[leaders[i]]):
                place += 1
        leaders.insert(place, name)
        leaderboard[name] = str(score)

leaderboardfile = open('leaderboard.txt', 'w')
for i in range(len(leaders)):
    leaderboardfile.write(leaders[i] + '\t' + leaderboard[leaders[i]] + '\n')

pygame.quit()
