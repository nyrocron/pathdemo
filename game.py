# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""game.py: contains the main game class that manages all other modules
            of the game"""

import pygame
from pygame import Rect

from camera import Camera
from events import EventManager
from input import InputManager
from rendering import Renderer
from map import Map
from objects.management import ObjectManager
from objects.gameobjects import Unit


class Game:
    """Manages other game modules."""

    def __init__(self):
        self._run = False
        self._last_update = 0

        self._mouse_drag_start = None
        self._selecting = False
        self._selection_rect = None
        self._mouse_right_down = False

        pygame.init()

        screen_size = (1024, 768)
        self._screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF)

        self._map = Map('default')
        self._camera = Camera(screen_size)
        self._renderer = Renderer(self._screen, self._camera)
        self._objects = ObjectManager(self._map.size)

        self._load()

        self._event_handler = EventManager()
        self._event_handler.subscribe(pygame.QUIT, self._handle_quit)
        self._event_handler.subscribe(self._camera.move_event,
                                      self._camera_moved)

        self._input_manager = InputManager(self._event_handler)
        self._input_manager.add_keybind(pygame.K_ESCAPE, self.stop)

        self._event_handler.subscribe(self._input_manager.mouse_drag_start,
                                      self._select_start)
        self._event_handler.subscribe(self._input_manager.mouse_drag_update,
                                      self._update_selection_rectangle)
        self._event_handler.subscribe(self._input_manager.mouse_drag_end,
                                      self._select_end)

    def run(self):
        """Run the main game loop."""
        self._last_update = 0

        self._run = True
        while self._run:
            self._update(pygame.time.get_ticks())
            self._draw()

        self._shutdown()

    def _load(self):
        unit_tex = self._renderer.load_texture('character.png')

        char_pos = (1, 1)
        char_rect = Rect(char_pos, self._renderer.texture_size(unit_tex))
        player_character = self._objects.create(Unit, char_rect)

        self._renderer.assign_texture(player_character, unit_tex)

    def _shutdown(self):
        pass

    def _update(self, gametime):
        time_passed = gametime - self._last_update
        if time_passed < 10:
            return

        self._event_handler.update()
        self._input_manager.update()
        self._objects.update(gametime)
        self._last_update = gametime

    def _camera_moved(self, event=None):
        if self._selecting:
            self._update_selection_rectangle()

    def _select_start(self, event=None):
        self._selecting = True
        self._update_selection_rectangle()

    def _select_end(self, event=None):
        self._selecting = False
        self._objects.select(self._selection_rect)

    def _update_selection_rectangle(self, event=None):
        # TODO handle all rect updates on game level
        self._selection_rect = self._camera.rect_to_map(
            self._input_manager.mouse_drag_rect)

    def _draw(self):
        self._screen.fill((0, 0, 0))  # clear black

        self._renderer.draw_map(self._map)

        objs = self._objects.query(self._camera.view_rect)
        self._renderer.draw_objects(objs)

        if self._selecting:
            self._renderer.draw_rectangle(self._selection_rect, (255, 0, 0))

        pygame.display.flip()

    def _draw_objects(self, surface, area):
        pass

    def _handle_quit(self, event):
        self.stop()

    def stop(self):
        self._run = False