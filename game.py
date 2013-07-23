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


class Game(object):
    """Manages other game modules."""

    def __init__(self):
        self._run = False
        self._last_update = 0

        self._last_mouse_pos = None
        self._selecting = False
        self._select_start_pos = None
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

        self._event_mgr = EventManager()
        self._event_mgr.subscribe(pygame.QUIT, self._handle_quit)
        self._event_mgr.subscribe(self._camera.move_event, self._camera_moved)

        self._input_manager = InputManager(self._event_mgr)
        self._input_manager.add_keybind(pygame.K_ESCAPE, self.stop)
        self._input_manager.add_keybind(pygame.K_q, self.stop)

        self._event_mgr.subscribe(self._input_manager.mouse_drag_start,
                                  self._select_start)
        self._event_mgr.subscribe(self._input_manager.mouse_drag_update,
                                  self._select_update)
        self._event_mgr.subscribe(self._input_manager.mouse_drag_end,
                                  self._select_end)
        self._event_mgr.subscribe(self._input_manager.rclick, self._rightclick)
        self._event_mgr.subscribe(self._input_manager.rsclick,
                                  self._right_shiftclick)

    def run(self):
        """Run the main game loop."""
        self._last_update = pygame.time.get_ticks()

        self._run = True
        while self._run:
            self._update(pygame.time.get_ticks())
            self._draw()

        self._shutdown()

    def _load(self):
        unit_tex = self._renderer.load_texture('cross.png')

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

        self._event_mgr.update()
        self._objects.update(gametime)
        self._camera.update(time_passed)

        self._last_update = gametime

    def _camera_moved(self, event):
        if self._selecting:
            self._update_selection_rectangle(self._last_mouse_pos)

    def _select_start(self, event):
        self._selecting = True
        self._select_start_pos = event.pos
        self._update_selection_rectangle(event.pos)

    def _select_end(self, event):
        self._selecting = False
        self._objects.select(self._selection_rect)

    def _select_update(self, event):
        self._last_mouse_pos = event.pos
        self._update_selection_rectangle(event.pos)

    def _update_selection_rectangle(self, pos):
        map_pos = self._camera.point_to_map(pos)
        self._selection_rect = Rect(min(self._select_start_pos[0], map_pos[0]),
                                    min(self._select_start_pos[1], map_pos[1]),
                                    abs(map_pos[0] - self._select_start_pos[0]),
                                    abs(map_pos[1] - self._select_start_pos[1]))

    def _rightclick(self, event):
        self._objects.send_selected(self._camera.point_to_map(event.pos))

    def _right_shiftclick(self, event):
        self._objects.send_selected(self._camera.point_to_map(event.pos), True)

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