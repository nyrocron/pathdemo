# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""input.py: input management"""

import pygame
from events import EventManager


class InputManager:
    MOUSE_LEFT = 1
    MOUSE_MIDDLE = 2
    MOUSE_RIGHT = 3

    def __init__(self, event_manager):
        event_manager.subscribe(pygame.KEYDOWN, self._key_down)
        event_manager.subscribe(pygame.KEYUP, self._key_up)

        event_manager.subscribe(pygame.MOUSEBUTTONDOWN, self._mouse_down)
        event_manager.subscribe(pygame.MOUSEBUTTONUP, self._mouse_up)
        event_manager.subscribe(pygame.MOUSEMOTION, self._mouse_moved)

        self._keybinds = {}

        self._mouse_left_is_down = False

        self.mouse_drag_start = EventManager.new_event_code()
        self.mouse_drag_end = EventManager.new_event_code()
        self.mouse_drag_update = EventManager.new_event_code()
        self.mouse_dragging = False
        self._mouse_drag_start = None

    def update(self):
        pass

    def add_keybind(self, key, callback):
        if not key in self._keybinds:
            self._keybinds[key] = set()
        self._keybinds[key].add(callback)

    def remove_keybind(self, key, callback):
        self._keybinds[key].remove(callback)

    def _key_down(self, event):
        try:
            for f in self._keybinds[event.key]:
                f()
        except KeyError:
            pass

    def _key_up(self, event):
        pass

    def _mouse_moved(self, event):
        if self._mouse_left_is_down:
            if self.mouse_dragging:
                EventManager.post(self.mouse_drag_update, pos=event.pos)
            else:
                self._mouse_drag_start = event.pos
                self.mouse_dragging = True
                EventManager.post(self.mouse_drag_start, pos=event.pos)

    def _mouse_down(self, event):
        if event.button == InputManager.MOUSE_LEFT:
            self._mouse_left_is_down = True

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
    #
    #    # mouse
    #    x, y = mouse.get_pos()
    #    pressed_buttons = mouse.get_pressed()
    #
    #    if pressed_buttons[0]:
    #        if not self._dragging:
    #            self._mouse_drag_start = self._camera.point_to_map(x, y)
    #            self._selection_rect = Rect(self._mouse_drag_start, (0, 0))
    #            self._dragging = True
    #    else:
    #        if self._dragging:
    #            self._mouse_dragged()
    #            self._dragging = False
    #
    #    if pressed_buttons[2]:
    #        if not self._mouse_right_down:
    #            self._mouse_right_down = True
    #    else:
    #        if self._mouse_right_down:
    #            if pressed_keys[pygame.K_LSHIFT]:
    #                self._mouse_right_shiftclicked(x, y)
    #            else:
    #                self._mouse_right_clicked(x, y)
    #            self._mouse_right_down = False
    #
    #    if self._mouse_last_pos is None or self._mouse_last_pos != (x, y):
    #        self._mouse_moved(x, y)
    #    self._mouse_last_pos = (x, y)
    #
    #def _mouse_right_clicked(self, x, y):
    #    self._objects.send_selected(self._camera.point_to_map(x, y))
    #
    #def _mouse_right_shiftclicked(self, x, y):
    #    self._objects.send_selected(self._camera.point_to_map(x, y), True)