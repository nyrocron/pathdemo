__author__ = 'Florian Tautz'

import pygame


class Game:
    def __init__(self):
        pygame.init()

        size = self._width, self._height = 1920, 1200
        self._speed = [2, 2]

        self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN|
                                                     pygame.DOUBLEBUF|
                                                     pygame.HWSURFACE)
        self._ball = pygame.image.load("ball.png")
        self._ball_rect = self._ball.get_rect()

        self._last_update = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update(pygame.time.get_ticks())
            self.draw()

    def update(self, game_time):
        time_passed = game_time - self._last_update
        if time_passed < 10:
            return
        self._last_update = game_time

        v = 0.2
        dx = self._speed[0] * (time_passed / (1/v))
        dy = self._speed[1] * (time_passed / (1/v))

        self._ball_rect = self._ball_rect.move(dx, dy)

        # keep ball in bounds
        if self._ball_rect.left < 0 or self._ball_rect.right > self._width:
            self._speed[0] *= -1
        if self._ball_rect.top < 0 or self._ball_rect.bottom > self._height:
            self._speed[1] *= -1

    def draw(self):
        self._screen.fill((255, 255, 255))
        self._screen.blit(self._ball, self._ball_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()

    def stop(self):
        exit()