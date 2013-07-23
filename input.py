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

        self._keybinds_down = {}
        self._keybinds_up = {}

        self._hot_area_ids = set()
        self._active_hotareas = set()
        self._hot_area_counter = 0
        self._hot_area_rects = {}
        self._hot_area_actions = {}

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

    def set_keybind(self, key, down_action=None, up_action=None):
        if down_action is not None:
            if not key in self._keybinds_down:
                self._keybinds_down[key] = set()
            self._keybinds_down[key].add(down_action)

        if up_action is not None:
            if not key in self._keybinds_up:
                self._keybinds_up[key] = set()
            self._keybinds_up[key].add(up_action)

    def unset_keybind(self, key, callback):
        self._keybinds_down[key].remove(callback)

    def set_hotarea(self, area, callback, args=None):
        """Set a hotarea and return its id.

        When the mouse moves into the specified area, the specified callback
        will be called. args can be a dict of arguments to be passed to
        the callback"""

        hotarea_id = self._new_hotarea_id()
        rect = pygame.Rect(area)

        self._hot_area_ids.add(hotarea_id)
        self._hot_area_rects[hotarea_id] = rect
        self._hot_area_actions[hotarea_id] = (callback,
                                              {} if args is None else args)

    def unset_hotarea(self, hotarea_id):
        """Unset hotarea with given id."""

        self._hot_area_ids.remove(hotarea_id)
        del self._hot_area_rects[hotarea_id]
        del self._hot_area_actions[hotarea_id]

    def _new_hotarea_id(self):
        self._hot_area_counter += 1
        return self._hot_area_counter

    def _key_down(self, event):
        self._pushed_keys.add(event.key)

        try:
            for action in self._keybinds_down[event.key]:
                action()
        except KeyError:
            pass

    def _key_up(self, event):
        self._pushed_keys.remove(event.key)

        try:
            for action in self._keybinds_up[event.key]:
                action()
        except KeyError:
            pass

    @property
    def _shift_pushed(self):
        return not self._pushed_keys.isdisjoint(InputManager.SHIFTKEYS)

    def _mouse_moved(self, event):
        pos = event.pos
        if self._mouse_left_is_down:
            if self.mouse_dragging:
                EventManager.post(self.mouse_drag_update, pos=pos)
            elif InputManager.MOUSE_DRAG_THRESHOLD < \
                    util.point_dist(self._mouse_left_down_pos, pos):
                self._mouse_drag_start = pos
                self.mouse_dragging = True
                EventManager.post(self.mouse_drag_start, pos=pos)

        current_active_hotareas = set()
        for hotarea_id in self._hot_area_ids:
            if self._hot_area_rects[hotarea_id].collidepoint(pos):
                current_active_hotareas.add(hotarea_id)

        entered_hotareas = current_active_hotareas - self._active_hotareas
        #left_hotareas = self._active_hotareas - current_active_hotareas

        for hotarea_id in entered_hotareas:
            callback, args = self._hot_area_actions[hotarea_id]
            callback(**args)

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