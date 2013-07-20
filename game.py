__author__ = 'Florian Tautz'

import pygame
from pygame import Rect

from camera import Camera
from rendering import Renderer, Texture
from map import Map
from objects.management import ObjectManager
from objects.gameobjects import Unit


class Game:
    def __init__(self):
        pygame.init()

        screen_size = self._width, self._height = 1024, 768
        self._screen = pygame.display.set_mode(screen_size,
                                               pygame.DOUBLEBUF)# |
                                               #pygame.FULLSCREEN |
                                               #pygame.HWSURFACE)

        self._map = Map('default')

        self._camera = Camera(screen_size)

        self._renderer = Renderer(self._screen, self._camera)

        self._objects = ObjectManager(self._map.rect)

        unit_tex = self._renderer.load_texture('character.png')

        char_pos = (1, 1)
        char_rect = Rect(char_pos, self._renderer.texture_size(unit_tex))
        self._player_character = self._objects.create(Unit, char_rect)

        self._renderer.assign_texture(self._player_character, unit_tex)

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

        delta = 0.25 * time_passed

        # camera movement
        if pressed_keys[pygame.K_w]:
            self._camera.move(0, -delta)
        if pressed_keys[pygame.K_s]:
            self._camera.move(0, delta)
        if pressed_keys[pygame.K_a]:
            self._camera.move(-delta, 0)
        if pressed_keys[pygame.K_d]:
            self._camera.move(delta, 0)

        # character movement
        if pressed_keys[pygame.K_UP]:
            self._objects.move_object(self._player_character, 0, -delta)
        if pressed_keys[pygame.K_DOWN]:
            self._objects.move_object(self._player_character, 0, delta)

        self._last_update = game_time

    def _draw(self):
        self._screen.fill((0, 0, 0)) # clear black
        view_rect = self._camera.rect
        #self._map.draw(self._screen, view_rect)
        objs = self._objects.query(view_rect)
        # if len(objs) == 0:
        #     raise Exception("no objects found")
        self._renderer.draw_objects(objs)
        pygame.display.flip()

    def _draw_objects(self, surface, area):
        pass

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()

    def stop(self):
        self._run = False