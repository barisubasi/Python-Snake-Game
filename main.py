import random
import time
import pygame
from pygame.locals import *

SIZE = 40
BACKROUND_COLOR=(96, 166, 67)
WINDOWX=1000
WINDOWY=600
applex=(WINDOWX/40)-1
appley=(WINDOWY/40)-1
class Apple:
    def __init__(self, screen):
        self.parent_screen = screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = random.randint(1, applex) * SIZE
        self.y = random.randint(1, appley) * SIZE

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()


    def move(self,snake):
        e = True
        x = random.randint(1, applex) * SIZE
        y = random.randint(1, appley) * SIZE
        while e:
            a = 0
            for i in range(len(snake.x)):
                if snake.x[i] == x and snake.y[i] == y:
                    x = random.randint(1, applex) * SIZE
                    y = random.randint(1, appley) * SIZE
                    a = 1

            if a == 0:
                e = False

        self.x = x
        self.y = y

class Snake:
    def __init__(self, parent_screen, lenght):
        self.lenght = lenght
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * lenght
        self.y = [SIZE] * lenght
        self.direction = 'right'

    def increase_lenght(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKROUND_COLOR)
        for i in range(self.lenght):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.lenght - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()
        self.sound=pygame.mixer.Sound("resources/theme music.mp3")
        self.applesound=pygame.mixer.Sound("resources/apple-eating.mp3")

        pygame.mixer.Sound.play(self.sound)
        self.surface = pygame.display.set_mode((WINDOWX,WINDOWY))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apples=[]
        self.create_apple(4)


    def create_apple(self,count):
        for i in range(count):
            self.apples.append(Apple(self.surface))
            self.apples[i].draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True

    def is_hit_wall(self):
        if self.snake.x[0]>WINDOWX or self.snake.x[0]<0:
            return True

        if self.snake.y[0]>WINDOWY or self.snake.y[0]<0:
            return True


    def play(self):
        self.snake.walk()
        for i in self.apples:
            i.draw()
        self.display_score()

        for i in self.apples:
            if self.is_collision(self.snake.x[0], self.snake.y[0],i.x, i.y):
                i.move(self.snake)
                self.snake.increase_lenght()
                pygame.mixer.Sound.play(self.applesound)

        if self.is_hit_wall():
            raise "GAME OVER"

        for i in range(3,self.snake.lenght):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise "GAME OVER"


    def show_game_over(self):
        pygame.mixer.Sound.stop(self.sound)
        self.bruhsound=pygame.mixer.Sound("resources/losing-theme.mp3")
        pygame.mixer.Sound.play(self.bruhsound)
        self.surface.fill(BACKROUND_COLOR)
        font = pygame.font.SysFont('Calibri', 30)
        line1=font.render(f"TOTAL SCORE: {self.snake.lenght}",True,(0,0,0))
        self.surface.blit(line1,(200,200))
        line3 = font.render(f"PRESS ENTER TO CONTINUE", True, (0, 0, 0))
        self.surface.blit(line3, (200, 400))
        line2=font.render(f"PRESS SPACE TO RESTART",True,(0,0,0))
        self.surface.blit(line2,(200,450))
        pygame.display.update()

    def display_score(self):
        font=pygame.font.SysFont('Calibri',30)
        score=font.render(f"Score: {self.snake.lenght}",True,(0,0,0))
        self.surface.blit(score,(800,10))
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.apple2 = Apple(self.surface)

    def run(self):
        pause=False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if not pause:
                        if event.key == K_UP or event.key == K_w:
                            self.snake.move_up()
                        if event.key == K_DOWN or event.key == K_s:
                            self.snake.move_down()
                        if event.key == K_LEFT or event.key == K_a:
                            self.snake.move_left()
                        if event.key == K_RIGHT or event.key == K_d:
                            self.snake.move_right()
                    else:
                        if event.key == K_RETURN:
                            pygame.mixer.Sound.stop(self.bruhsound)
                            pygame.mixer.Sound.play(self.sound)
                            pause = False
                        if event.key==K_SPACE:
                            pygame.mixer.Sound.stop(self.bruhsound)
                            pygame.mixer.Sound.play(self.sound)
                            self.reset()
                            pause=False


                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True

            time.sleep(0.15)


game = Game()
game.run()
