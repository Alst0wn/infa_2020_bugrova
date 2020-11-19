import pygame
from pygame.draw import *
from random import randrange as rnd, choice
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (100, 60, 20)
ORANGE = (255, 100, 0)

class ball():
    def __init__(self, vx, vy):
        """ Конструктор класса ball

        Args:
        vx - начальная скорость мяча по горизонтали
        vy - начальная скорость мяча по вертикали
        
        """
        self.x = 40
        self.y = 450
        self.r = 15
        self.vx = vx
        self.vy = vy
        self.color = choice([BLUE, GREEN, RED, BROWN])
        self.live = FPS*3

    def move(self, g=2):
        """Переместить мяч по прошествии единицы времени и рисует его.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x < (0 + self.r):
            self.vx = - self.vx
            self.x = (0 + self.r)
            self.vx = int(self.vx*0.7)
            self.vy = int(self.vy*0.7)
        if self.x > (800 - self.r):
            self.vx = - self.vx
            self.x = (800 - self.r)
            self.vx = int(self.vx*0.7)
            self.vy = int(self.vy*0.7)
        if self.y < (0 + self.r):
            self.vy = - self.vy
            self.y = (0 + self.r)
            self.vx = int(self.vx*0.7)
            self.vy = int(self.vy*0.7)
        if self.y > (600 - self.r):
            self.vy = - self.vy
            self.y = (600 - self.r)
            self.vx = int(self.vx*0.7)
            self.vy = int(self.vy*0.7)
        self.vy -= g
        self.live -= 1
        if self.live > 0:
            circle(screen, self.color, (self.x, self.y), self.r)
            circle(screen, BLACK, (self.x, self.y), self.r, 1)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (obj.x - self.x)*(obj.x - self.x)+\
                    (obj.y - self.y)*(obj.y - self.y) <\
                    (obj.r + self.r)*(obj.r + self.r)


class gun():
    def __init__(self):
        """ Конструктор класса gun
        """
        self.f2_power = 10
        self.f2_on = False
        self.an = 1
    
    def fire2_start(self):
        """Функция начинает усиливание пушки
        """
        self.f2_on = True

    def fire2_end(self, event, balls, bullet):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        Принимает отпускание мыши, массив шаров и количество пуль
        """
        bullet += 1
        self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 40))
        new_ball = ball(int(self.f2_power * math.cos(self.an)), - int(self.f2_power * math.sin(self.an)))
        balls.append(new_ball)
        self.f2_on = False
        self.f2_power = 10
        return balls, bullet

    def targetting(self, mouse):
        """Прицеливание. Зависит от положения мыши.
        
        Args:
        mouse - pygame.mouse, положение мыши
        """
        self.an = math.atan((mouse.get_pos()[1]-450) / (mouse.get_pos()[0]-20))
        if self.f2_on:
            line (screen, ORANGE, (20, 450),
                    (20 + int(max(self.f2_power, 20) * math.cos(self.an)),
                    450 + int(max(self.f2_power, 20) * math.sin(self.an))),
                    7)
        else:
            line (screen, BLACK, (20, 450),
                    (20 + int(max(self.f2_power, 20) * math.cos(self.an)),
                    450 + int(max(self.f2_power, 20) * math.sin(self.an))),
                    7)

    def power_up(self):
        """Функция усиливает пушку после прицеливания
        """
        if self.f2_on and self.f2_power < 100:
                self.f2_power += 1


class target():
    def __init__(self, ts):
        """ Конструктор класса target
        Берет как аргумент список уже существующиющих целей
        """
        x=self.x = rnd(600, 780)
        y=self.y = rnd(300, 550)
        r=self.r = rnd(20, 50)
        self.vx = rnd(-3,3)
        self.vy = rnd(-3, 3)
        color=self.color = RED

    def move(self):
        """Переместить цель по прошествии единицы времени и рисует его.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям окна.
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x < (0 + self.r):
            self.vx = - self.vx
            self.x = (0 + self.r)
        if self.x > (800 - self.r):
            self.vx = - self.vx
            self.x = (800 - self.r)
        if self.y < (0 + self.r):
            self.vy = - self.vy
            self.y = (0 + self.r)
        if self.y > (600 - self.r):
            self.vy = - self.vy
            self.y = (600 - self.r)
        circle(screen, self.color, (self.x, self.y), self.r)
        circle(screen, BLACK, (self.x, self.y), self.r, 1)



g1 = gun()
ts=[]
bullet = 0
balls = []
pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = 0

def new_game(score):
    g1.f2_on = False
    ts=[]
    paused = False
    bullet = 0
    balls = []
    for i in range(12):
        ts.append(target(ts))
    while len(ts) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, score
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 750 and event.pos[0] < 790\
                        and event.pos[1] > 10 and event.pos[1] < 30:
                    paused = True
                else:
                    g1.fire2_start()
            if event.type == pygame.MOUSEBUTTONUP and g1.f2_on:
                balls, bullet = g1.fire2_end(event, balls, bullet)
        for b in balls:
            b.move()
            k=0
            for i in range(len(ts)):
                if b.hittest(ts[i-k]) and b.live > 0:
                    ts.pop(i-k)
                    k += 1
                    score += 1
        if paused:
            surf = pygame.Surface((800, 600), pygame.SRCALPHA)
            rect(surf, (0, 0 ,0 , 100), (0, 0, 800, 600))
            screen.blit(surf, (0, 0))
        while paused:
            rect(screen, MAGENTA, (200, 50, 400, 100))
            screen.blit(pygame.font.Font(None, 60).render('Continue', 1, BLACK), (250, 70))
            rect(screen, MAGENTA, (200, 250, 400, 100))
            screen.blit(pygame.font.Font(None, 60).render('New game', 1, BLACK), (250, 270))
            rect(screen, MAGENTA, (200, 450, 400, 100))
            screen.blit(pygame.font.Font(None, 60).render('Exit', 1, BLACK), (250, 470))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True, score
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] > 200 and event.pos[0] < 600\
                            and event.pos[1] > 50 and event.pos[1] < 150:
                        paused = False
                    if event.pos[0] > 200 and event.pos[0] < 600\
                            and event.pos[1] > 250 and event.pos[1] < 350:
                        screen.fill(WHITE)
                        clock.tick(FPS)
                        screen.blit(pygame.font.Font(None, 28).render('Вы не уничтожили все цели '\
                               , 1, BLACK), (100, 300))
                        pygame.display.update()
                        for i in range(FPS*3):
                            clock.tick(FPS)
                        return False, score
                    if event.pos[0] > 200 and event.pos[0] < 600\
                            and event.pos[1] > 450 and event.pos[1] < 550:
                        return True, score
            clock.tick(FPS)        
            
        clock.tick(FPS)
        rect(screen, MAGENTA, (750, 10, 40, 20))
        screen.blit(pygame.font.Font(None, 18).render('Pause', 1, BLACK), (753, 12))
        pygame.display.update()
        screen.fill(WHITE)
        for t in ts:
            t.move()
        screen.blit(pygame.font.Font(None, 40).render(str(score), 1, BLACK), (20, 20))
        g1.power_up()
        g1.targetting(pygame.mouse)
        
    screen.fill(WHITE)
    clock.tick(FPS)
    screen.blit(pygame.font.Font(None, 28).render('Вы уничтожили цели за '\
        + str(bullet) + ' выстрелов', 1, BLACK), (100, 300))
    pygame.display.update()
    for i in range(FPS*3):
        clock.tick(FPS)
    return False, score

while not finished:
    finished, score = new_game(0)



pygame.quit()
