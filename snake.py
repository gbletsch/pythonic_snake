import pygame
from pygame.locals import *
from pygame.math import Vector2
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

SIZE = 10

class Snake:
    size = (SIZE, SIZE)

    def __init__(self, position):
        self.image = pygame.Surface(self.size)
        self.image.fill(GREEN)
        self.rects = [self.image.get_rect(), self.image.get_rect()]
        self.rects[0].topleft = position
        self.speed = Vector2()


class Apple(pygame.sprite.Sprite):
    """
    Parameters
    ----------
    position: tuple (x, y)
    """
    size = (SIZE, SIZE)

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.size)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = position


class Text:
    GAME_FONT = ('arial', 24)

    '''Params: x, y, value, color'''
    def __init__(self, x, y, text, color, size=(150, 50)):
        self.size = size
        self.image = pygame.Surface(self.size)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(*self.GAME_FONT)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



class App:
    size = width, height = (200, 200)
    fps = 8

    def __init__(self):
        self._running = True
        self._screen = None
        self._snake = None
        self.apple = Apple(self.put_on_grid(random.randint(0, self.width - 1),
                                            random.randint(0, self.height - 1)))
        self.snake = Snake(self.put_on_grid(random.randint(0, self.width - 1),
                                            random.randint(0, self.height - 1)))
        self.velocity = SIZE
        self._clock = None

    def put_on_grid(self, x, y):
        x = (x // SIZE) * SIZE
        y = (y // SIZE) * SIZE
        return x, y

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Phytonic Snake')
        self._clock = pygame.time.Clock()
        self._screen.fill(BLACK)
        start_msg = Text(x=self._screen.get_width() // 2,
                         y=self._screen.get_height() // 2,
                         text='Press any key', color=RED)
        sm = start_msg.font.render(start_msg.text, True, start_msg.color)
        self._screen.blit(sm, start_msg.rect)
        pygame.display.update()
        pygame.event.clear()
        event = pygame.event.wait()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        if event.key == K_ESCAPE:
            self._running = False
        elif event.key == K_UP and self.snake.speed != Vector2(0, self.velocity):
            self.snake.speed = Vector2(0, - self.velocity)
        elif event.key == K_DOWN and self.snake.speed != Vector2(0, - self.velocity):
            self.snake.speed = Vector2(0, self.velocity)
        elif event.key == K_RIGHT and self.snake.speed != Vector2(- self.velocity, 0):
            self.snake.speed = Vector2(self.velocity, 0)
        elif event.key == K_LEFT and self.snake.speed != Vector2(self.velocity, 0):
            self.snake.speed = Vector2(- self.velocity, 0)

    def on_loop(self):
        self.on_update()

    def on_collide(self):
        # eat apple
        if self.snake.rects[0].colliderect(self.apple.rect):
            self.snake.rects.append(self.snake.rects[-1].copy())
            # del(self.apple)
            self.apple = Apple(self.put_on_grid(random.randint(0, self.width - 1),
                                                random.randint(0, self.height - 1)))
        # die...
        if self.snake.rects[0].bottom > self._screen.get_height() or \
           self.snake.rects[0].top < 0 or \
           self.snake.rects[0].right > self._screen.get_width() or \
           self.snake.rects[0].left < 0 or \
           self.snake.rects[0].collidelist(self.snake.rects[2:-1]) != -1: # hit itself
            self.on_game_over()

    def on_game_over(self):
        end_msg = Text(x=self._screen.get_width() // 2,
                         y=self._screen.get_height() // 3,
                         text='Game over', color=BLUE)
        end_msg_2 = Text(x=self._screen.get_width() // 2,
                       y=self._screen.get_height() // 3 * 2,
                       text='Continue? (y/n)', color=BLUE)

        em = end_msg.font.render(end_msg.text, True, end_msg.color)
        em2 = end_msg_2.font.render(end_msg_2.text, True, end_msg_2.color)
        self._screen.blits((
            (em, end_msg.rect),
            (em2, end_msg_2.rect)
        ))
        pygame.display.update()
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_y:
                self._screen.fill(BLACK)
                pygame.display.flip()
                pygame.quit()
                app = App()
                app.on_execute()

        self.on_quit()


    def on_update(self):
        # move snake
        self.snake.rects[0].move_ip(self.snake.speed)
        for i in range(len(self.snake.rects) - 1, 0, -1):
            self.snake.rects[i].topleft = self.snake.rects[i - 1].topleft
        # verify collisions
        self.on_collide()

    def on_render(self):
        self._screen.fill(BLACK)
        self._screen.blit(self.apple.image, self.apple.rect)
        for piece in self.snake.rects:
            self._screen.blit(self.snake.image, piece)
        pygame.display.flip()

    def on_quit(self):
        pygame.quit()
        quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            self._clock.tick(self.fps)
            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.on_event(event)

            self.on_loop()
            self.on_render()

        # self.on_quit()
        self.on_game_over()

if __name__ == '__main__':
    app = App()
    app.on_execute()