# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""game.py: manages all other modules of the game"""

import pygame
from pygame import Rect

from camera import Camera
from events import EventManager
from input import InputManager
from rendering import Renderer
from map import Map
from gameobjects.management import ObjectManager
from gameobjects.gameobjects import Unit


class Game(object):
    """Manages other game modules."""

    def __init__(self, min_cycle_time=10):
        self.min_cycle_time = min_cycle_time

        self._run = False
        self._last_update = 0

        self._last_mouse_pos = None
        self._selecting = False
        self._select_start_pos = None
        self._selection_rect = None
        self._mouse_right_down = False

        pygame.init()

        screen_width, screen_height = screen_size = (1024, 768)
        self._screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF)

        self._map = Map('default')
        self._camera = Camera(screen_size)
        self._renderer = Renderer(self._screen, self._camera)
        self._objects = ObjectManager(self._map.size)

        self._event_mgr = EventManager()
        self._event_mgr.subscribe(pygame.QUIT, self._handle_quit)
        self._event_mgr.subscribe(self._camera.move_event, self._camera_moved)

        self._input = InputManager(self._event_mgr)
        self._input.set_keybind(pygame.K_ESCAPE, self.stop)
        self._input.set_keybind(pygame.K_q, self.stop)

        self._input.set_hotarea((0, 0, screen_width, 2),
                                self._camera.set_move, {'y': -1})
        self._input.set_hotarea((0, screen_height - 2, screen_width, 2),
                                self._camera.set_move, {'y': 1})
        self._input.set_hotarea((0, 0, 2, screen_height - 2),
                                self._camera.set_move, {'x': -1})
        self._input.set_hotarea((screen_width - 2, 0, 2, screen_height),
                                self._camera.set_move, {'x': 1})
        self._input.set_hotarea((2, 2, screen_width - 4, screen_height - 4),
                                self._camera.stop_moving)

        self._event_mgr.subscribe(self._input.mouse_drag_start,
                                  self._select_start)
        self._event_mgr.subscribe(self._input.mouse_drag_update,
                                  self._select_update)
        self._event_mgr.subscribe(self._input.mouse_drag_end,
                                  self._select_end)

        self._event_mgr.subscribe(self._input.lclick, self._leftclick)
        self._event_mgr.subscribe(self._input.rclick, self._rightclick)
        self._event_mgr.subscribe(self._input.rsclick,
                                  self._right_shiftclick)

    def run(self):
        """Run the main game loop."""
        self._load()
        self._last_update = pygame.time.get_ticks()

        self._run = True
        while self._run:
            gametime = pygame.time.get_ticks()
            time_passed = gametime - self._last_update

            if time_passed < self.min_cycle_time:
                pygame.time.wait(1)  # give other threads some cpu time
                continue

            self._update(gametime, time_passed)
            self._draw()

        self._shutdown()

    def _load(self):
        unit_tex = self._renderer.load_texture('cross.png')

        for x in range(0, 48, 16):
            unit_pos = (x, 16)
            unit_rect = Rect(unit_pos, self._renderer.texture_size(unit_tex))
            unit_id = self._objects.create(Unit, unit_rect)
            self._renderer.assign_texture(unit_id, unit_tex)

    def _shutdown(self):
        pass

    def _update(self, gametime, time_passed):
        self._event_mgr.update()
        self._objects.update(gametime)
        self._camera.update(time_passed)

        self._last_update = gametime

    #noinspection PyUnusedLocal
    def _camera_moved(self, event):
        if self._selecting:
            self._update_selection_rectangle(self._last_mouse_pos)

    def _select_start(self, event):
        self._selecting = True
        self._select_start_pos = event.pos
        self._update_selection_rectangle(event.pos)

    #noinspection PyUnusedLocal
    def _select_end(self, event):
        self._selecting = False
        self._objects.select_area(self._selection_rect)

    def _select_update(self, event):
        self._last_mouse_pos = event.pos
        self._update_selection_rectangle(event.pos)

    def _update_selection_rectangle(self, pos):
        map_pos = self._camera.point_to_map(pos)
        self._selection_rect = Rect(min(self._select_start_pos[0], map_pos[0]),
                                    min(self._select_start_pos[1], map_pos[1]),
                                    abs(map_pos[0] - self._select_start_pos[0]),
                                    abs(map_pos[1] - self._select_start_pos[1]))

    def _leftclick(self, event):
        self._objects.select_at(self._camera.point_to_map(event.pos))

    def _rightclick(self, event):
        self._objects.send_selected(self._camera.point_to_map(event.pos))

    def _right_shiftclick(self, event):
        self._objects.send_selected(self._camera.point_to_map(event.pos), True)

    def _draw(self):
        self._renderer.frame_start()

        self._renderer.draw_map(self._map)

        objs = self._objects.query(self._camera.view_rect)
        self._renderer.draw_objects(objs)

        if self._selecting:
            self._renderer.draw_rectangle(self._selection_rect, (255, 0, 0))

        self._renderer.frame_end()

    def _draw_objects(self, surface, area):
        pass

    #noinspection PyUnusedLocal
    def _handle_quit(self, event):
        self.stop()

    def stop(self):
        self._run = False