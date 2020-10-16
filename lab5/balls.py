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

def new_square():
    '''
    function generates a square - squares get faster and change directions when you click
    returns a square
    a square - tuple (x, y, vx, vy, a, i, life)
    x, y - coordinates of the left top corner of the square
    vx, vy - base speed of the square (square gets faster)
    a - size of the square
    i - number of the square's color in COLOR
    life - amount of tics ball have left to live
    all parameters are randomized
    '''
    x = randint(100 + speedrange + 50, 700 - speedrange - 50)
    y = randint(100 + speedrange + 50, 500 - speedrange - 50)
    vx = randint (-speedrange, speedrange)
    vy = randint (-speedrange, speedrange)
    a = randint(60,100)
    i = randint(0, 5)
    life = randint(lifespan//2, lifespan)
    return(x, y, vx, vy, a, i, life)


def new_ball():
    '''
    function generates a ball
    returns a ball
    a ball - tuple (x, y, vx, vy, r, i, life)
    x, y - coordinates of the new ball
    vx, vy - speed of the ball
    r - radius of the ball
    i - number of the ball's color in COLOR
    life - amount of tics ball have left to live
    all parameters are randomized
    '''
    x = randint(100 + speedrange + 50, 700 - speedrange - 50)
    y = randint(100 + speedrange + 50, 500 - speedrange - 50)
    vx = randint (-speedrange, speedrange)
    vy = randint (-speedrange, speedrange)
    r = randint(30,50)
    i = randint(0, 5)
    life = randint(lifespan//2, lifespan)
    return(x, y, vx, vy, r, i, life)


def moveball(ball):
    '''
    function moves a ball
    takes a ball
    returns a moved ball
    ball is refered in new_ball
    '''
    x, y, vx, vy, r, i, l = ball
    x += vx
    y += vy
    if x < (100 + r):
        vx = - vx
        x = (100 + r)
    if x > (700 - r):
        vx = - vx
        x = (700 - r)
    if y > (500 - r):
        vy = - vy 
        y = (500 - r)
    if y < (100 + r):
        vy = - vy
        y = (100 + r)
    return(x, y, vx, vy, r, i, l-1)

   
def movesquare(square):
    '''
    function moves a square
    takes a square
    returns a moved square
    square is refered in new_square
    '''
    x, y, vx, vy, a, i, l = square
    x += int(vx * (1 + (lifespan-l)/lifespan))
    y += int(vy * (1 + (lifespan-l)/lifespan))
    if x < (100):
        vx = - vx
        x = (100)
    if x > (700 - a):
        vx = - vx
        x = (700 - a)
    if y > (500 - a):
        vy = - vy 
        y = (500 - a)
    if y < (100):
        vy = - vy
        y = (100)
    return(x, y, vx, vy, a, i, l-1)


def drawball(ball):
    '''
    function draws a ball
    takes a ball and draws it on screen
    ball is refered in new_ball
    '''
    x, y, r, i = ball[0], ball[1], ball[4], ball[5]
    circle(screen, COLOR[i], (x, y), r)


def drawsquare(square):
    '''
    function draws a square
    takes a square and draws it on screen
    square is refered in new_square
    '''
    x, y, a, i = square[0], square[1], square[4], square[5]
    rect(screen, COLOR[i], (x, y, a, a))


def clickball(event, balls):
    '''
    function processes a click relative to balls
    takes an event (type mousebuttondown) and list of balls
    checks if click is inside of any balls if yes deletes those balls
    returns new list of balls and number of balls deleted
    ball is refered in new_ball
    '''
    hit = []
    xmouse, ymouse = event.pos
    for i in range(len(balls)):
        x, y, r = balls[i][0], balls[i][1], balls[i][4]
        if (xmouse-x)*(xmouse-x) + (ymouse-y)*(ymouse-y) < r*r:
            hit.append(i)
    for i in range(len(hit)):
        balls.pop(hit[i]-i)
    return(balls, len(hit))


def clicksquare(event, squares):
    '''
    function processes a click relative to squares
    takes an event (type mousebuttondown) and list of squares
    checks if click is inside of any squares if yes deletes those squares
    reverse the speed of every square
    returns new list of squares and number of squares deleted
    square is refered in new_square
    '''
    hit = []
    xmouse, ymouse = event.pos
    for i in range(len(squares)):
        x, y, vx, vy, a, s, l = squares[i]
        if xmouse > x and xmouse < (x+a) and ymouse > y and ymouse < (y+a):
            hit.append(i)
        squares[i] = (x, y, -vx, -vy, a, s, l)
    for i in range(len(hit)):
        squares.pop(hit[i]-i)
    return(squares, len(hit))


def death(objects):
    '''
    function deletes objects that exceed their lifespan
    takes a list of objects
    checks if any objects lived longer than their lifespan if yes deletes those objects
    returns new list of objects
    objects are refered in new_ball and new_square
    '''
    dead = []
    for i in range(len(objects)):
        l = objects[i][6]
        if l < 0:
            dead.append(i)
    for i in range(len(dead)):
        objects.pop(dead[i]-i)
    return(objects)


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

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished: #gameplay
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls, k = clickball(event, balls)
            squares, m = clicksquare(event, squares)
            score += ballscore*k + squarescore*m
    if len(balls) < 6:
        balls.append(new_ball())
    if len(squares) < 6:
        squares.append(new_square())
    balls = death(balls)
    squares = death(squares)
    for i in range(len(balls)):
        balls[i] = moveball(balls[i])
        drawball(balls[i])
    for i in range(len(squares)):
        squares[i] = movesquare(squares[i])
        drawsquare(squares[i])
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
