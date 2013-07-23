# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""input.py: input management"""

import pygame
import util
from events import EventManager

class InputManager(object):
    """Manages keyboard and mouse input."""
    MOUSE_LEFT = 1
    MOUSE_MIDDLE = 2
    MOUSE_RIGHT = 3

    MOUSE_DRAG_THRESHOLD = 3

    SHIFTKEYS = {pygame.K_LSHIFT, pygame.K_RSHIFT}

    def __init__(self, event_manager):
        event_manager.subscribe(pygame.KEYDOWN, self._key_down)
        event_manager.subscribe(pygame.KEYUP, self._key_up)

        event_manager.subscribe(pygame.MOUSEBUTTONDOWN, self._mouse_down)
        event_manager.subscribe(pygame.MOUSEBUTTONUP, self._mouse_up)
        event_manager.subscribe(pygame.MOUSEMOTION, self._mouse_moved)

        self._keybinds = {}
        self._hot_areas = {}

        self._pushed_keys = set()

        self._mouse_left_is_down = False
        self._mouse_left_down_pos = None

        # events
        self.lclick = EventManager.new_event_code()
        self.lsclick = EventManager.new_event_code()
        self.rclick = EventManager.new_event_code()
        self.rsclick = EventManager.new_event_code()

        self.mouse_drag_start = EventManager.new_event_code()
        self.mouse_drag_end = EventManager.new_event_code()
        self.mouse_drag_update = EventManager.new_event_code()

        self.mouse_dragging = False
        self._mouse_drag_start = None

    def add_keybind(self, key, callback):
        if not key in self._keybinds:
            self._keybinds[key] = set()
        self._keybinds[key].add(callback)

    def remove_keybind(self, key, callback):
        self._keybinds[key].remove(callback)

    def add_mouse_action(self, area, callback):
        pass  # TODO: implement hot area binding

    def _key_down(self, event):
        self._pushed_keys.add(event.key)
        try:
            for f in self._keybinds[event.key]:
                f()
        except KeyError:
            pass

    def _key_up(self, event):
        self._pushed_keys.remove(event.key)
        pass

    @property
    def _shift_pushed(self):
        return not self._pushed_keys.isdisjoint(InputManager.SHIFTKEYS)

    def _mouse_moved(self, event):
        if self._mouse_left_is_down:
            if self.mouse_dragging:
                EventManager.post(self.mouse_drag_update, pos=event.pos)
            elif InputManager.MOUSE_DRAG_THRESHOLD <\
                    util.point_dist(self._mouse_left_down_pos, event.pos):
                self._mouse_drag_start = event.pos
                self.mouse_dragging = True
                EventManager.post(self.mouse_drag_start, pos=event.pos)

        # TODO: implement hot areas

    def _mouse_down(self, event):
        if event.button == InputManager.MOUSE_LEFT:
            self._mouse_left_is_down = True
            self._mouse_left_down_pos = event.pos

            click_event = self.lsclick if self._shift_pushed else self.lclick
            EventManager.post(click_event, pos=event.pos)

        elif event.button == InputManager.MOUSE_RIGHT:
            click_event = self.rsclick if self._shift_pushed else self.rclick
            EventManager.post(click_event, pos=event.pos)

    def _mouse_up(self, event):
        if event.button == InputManager.MOUSE_LEFT:
            self._mouse_left_is_down = False

            if self.mouse_dragging:
                self.mouse_dragging = False
                EventManager.post(self.mouse_drag_end)

    #def _handle_input(self, time_passed):
    #    pressed_keys = pygame.key.get_pressed()
    #
    #    delta = 0.25 * time_passed
    #
    #    # camera movement
    #    if pressed_keys[pygame.K_w]:
    #        self._camera.move(0, -delta)
    #    if pressed_keys[pygame.K_s]:
    #        self._camera.move(0, delta)
    #    if pressed_keys[pygame.K_a]:
    #        self._camera.move(-delta, 0)
    #    if pressed_keys[pygame.K_d]:
    #        self._camera.move(delta, 0)
    #    self._camera_moved()