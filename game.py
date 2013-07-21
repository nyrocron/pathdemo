__author__ = 'Florian Tautz'

import pygame
from pygame import Rect, mouse

from camera import Camera
from rendering import Renderer
from map import Map
from objects.management import ObjectManager
from objects.gameobjects import Unit


class Game:
    def __init__(self):
        pygame.init()

        screen_size = (1024, 768)
        self._screen = pygame.display.set_mode(screen_size,
                                               pygame.DOUBLEBUF)# |
                                               #pygame.FULLSCREEN |
                                               #pygame.HWSURFACE)

        self._map = Map('default')
        self._camera = Camera(screen_size)
        self._renderer = Renderer(self._screen, self._camera)
        self._objects = ObjectManager(self._map.size)

        self._initialize()
        self._load()

    def run(self):
        self._last_update = 0

        self._run = True
        while self._run:
            for event in pygame.event.get():
                self._handle_event(event)

            self._update(pygame.time.get_ticks())
            self._draw()

    def _initialize(self):
        self._mouse_last_pos = None
        self._mouse_drag_start = None
        self._dragging = False
        self._selection_rect = None
        self._mouse_right_down = False

    def _load(self):
        unit_tex = self._renderer.load_texture('character.png')

        char_pos = (1, 1)
        char_rect = Rect(char_pos, self._renderer.texture_size(unit_tex))
        self._player_character = self._objects.create(Unit, char_rect)

        self._renderer.assign_texture(self._player_character, unit_tex)

    def _update(self, game_time):
        time_passed = game_time - self._last_update
        if time_passed < 10:
            return

        self._handle_mouse()
        self._handle_keyboard(time_passed)

        self._last_update = game_time

    def _handle_mouse(self):
        x, y = mouse.get_pos()
        pressed_buttons = mouse.get_pressed()

        if pressed_buttons[0]:
            if not self._dragging:
                self._mouse_drag_start = self._camera.point_to_map(x, y)
                self._selection_rect = Rect(self._mouse_drag_start, (0, 0))
                self._dragging = True
        else:
            if self._dragging:
                self._mouse_dragged()
                self._dragging = False

        if pressed_buttons[2]:
            if not self._mouse_right_down:
                self._mouse_right_down = True
        else:
            if self._mouse_right_down:
                self._mouse_right_clicked(x, y)
                self._mouse_right_down = False

        if self._mouse_last_pos is None or self._mouse_last_pos != (x, y):
            self._mouse_moved(x, y)
        self._mouse_last_pos = (x, y)

    def _mouse_dragged(self):
        self._objects.select(self._camera.rect_to_map(self._selection_rect))

    def _mouse_right_clicked(self, x, y):
        map_x, map_y = self._camera.point_to_map(x, y)
        self._objects.send_selected(map_x, map_y)

    def _mouse_moved(self, x, y):
        if self._dragging:
            self._update_selection_rect(x, y)

    def _update_selection_rect(self, x, y):
        map_x, map_y = self._camera.point_to_map(x, y)
        self._selection_rect = Rect(min(self._mouse_drag_start[0], map_x),
                                    min(self._mouse_drag_start[1], map_y),
                                    abs(map_x - self._mouse_drag_start[0]),
                                    abs(map_y - self._mouse_drag_start[1]))

    def _handle_keyboard(self, time_passed):
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
        self._camera_moved()

        # character movement
        if pressed_keys[pygame.K_UP]:
            self._objects.move_object(self._player_character, 0, -delta)
        if pressed_keys[pygame.K_DOWN]:
            self._objects.move_object(self._player_character, 0, delta)
        if pressed_keys[pygame.K_LEFT]:
            self._objects.move_object(self._player_character, -delta, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self._objects.move_object(self._player_character, delta, 0)

    def _camera_moved(self):
        if self._dragging:
            x, y = mouse.get_pos()
            self._update_selection_rect(x, y)

    def _draw(self):
        self._screen.fill((0, 0, 0)) # clear black

        self._renderer.draw_map(self._map)

        objs = self._objects.query(self._camera.view_rect)
        self._renderer.draw_objects(objs)

        if self._dragging and self._selection_rect is not None:
            self._renderer.draw_rectangle(self._selection_rect, (255, 0, 0))

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