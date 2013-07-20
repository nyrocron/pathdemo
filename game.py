__author__ = 'Florian Tautz'

import pygame

from camera import Camera
from map import Map


class Game:
    def __init__(self):
        pygame.init()

        size = self._width, self._height = 1024, 768
        self._speed = [2, 2]

        self._screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)# |
                                                     #pygame.FULLSCREEN |
                                                     #pygame.HWSURFACE)

        self._camera = Camera(size)
        self._map = Map('default')
        cx, cy = self._map.get_center()
        self._camera.center_on(cx, cy)

    def run(self):
        self._last_update = 0

        self._run = True
        while self._run:
            for event in pygame.event.get():
                self._handle_event(event)

            self._update(pygame.time.get_ticks())
            self._draw()

    def _update(self, game_time):
        time_passed = game_time - self._last_update
        if time_passed < 10:
            return

        pressed_keys = pygame.key.get_pressed()

        # camera movement
        delta = 0.25 * time_passed
        if pressed_keys[pygame.K_w]:
            self._camera.move(0, -delta)
        if pressed_keys[pygame.K_s]:
            self._camera.move(0, delta)
        if pressed_keys[pygame.K_a]:
            self._camera.move(delta, 0)
        if pressed_keys[pygame.K_d]:
            self._camera.move(-delta, 0)

        self._last_update = game_time

    def _draw(self):
        self._screen.fill((0, 0, 0)) # clear black
        self._map.draw(self._screen, self._camera.get_view_rect())
        pygame.display.flip()

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()

    def stop(self):
        self._run = False