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
    def __init__(self):
        """ Конструктор класса target
        """
        self.points = 0
        self.live = 1
        x=self.x = rnd(600, 780)
        y=self.y = rnd(300, 550)
        r=self.r = rnd(20, 50)
        self.vx = choice([1, -1])
        self.vy = choice([1, -1])
        color=self.color = RED

    def draw(self):
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
        if self.live == 1:
            circle(screen, self.color, (self.x, self.y), self.r)
            circle(screen, BLACK, (self.x, self.y), self.r, 1)
   
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.x = rnd(600, 780) 
        self.y = rnd(300, 550)
        self.r = rnd(20, 50)
        self.points += points


g1 = gun()
t1 = target()
t2 = target()
t3 = target()
bullet = 0
balls = []
pygame.display.update()
clock = pygame.time.Clock()
finished = False


def new_game():
    bullet = 0
    balls = []

    
    t1.live = 1
    t2.live = 1
    t3.live = 1
    while t1.live or t2.live or t3.live:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                g1.fire2_start()
            if event.type == pygame.MOUSEBUTTONUP:
                balls, bullet = g1.fire2_end(event, balls, bullet)
        for b in balls:
            b.move()
            for t in [t1, t2, t3]:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.hit()
        clock.tick(FPS)
        pygame.display.update()
        screen.fill(WHITE)
        t1.draw()
        t2.draw()
        t3.draw()
        screen.blit(pygame.font.Font(None, 40).render(str(t1.points+t2.points+t3.points), 1, BLACK), (20, 20))
        g1.power_up()
        g1.targetting(pygame.mouse)
    screen.fill(WHITE)
    clock.tick(FPS)
    screen.blit(pygame.font.Font(None, 28).render('Вы уничтожили цели за '\
        + str(bullet) + ' выстрелов', 1, BLACK), (100, 300))
    pygame.display.update()
    for i in range(FPS*3):
        clock.tick(FPS)
    return False

while not finished:
    finished = new_game()

pygame.quit()
