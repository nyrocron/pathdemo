# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""camera.py: camera management"""

from pygame import Rect
from events import EventManager
import util


class Camera(object):
    """Manages current view rectangle and provides methods to convert
    coordinates from/to screen/map coordinate systems."""

    MOVE_SPEED = 0.25

    def __init__(self, view_size):
        self.view_rect = Rect((0, 0), view_size)
        self.move_event = EventManager.new_event_code()

        self._moving = False
        self._move_vector = [0, 0]

        self._last_update = 0

    def update(self, time_passed):
        """Update camera.

        Execute movement and such"""

        if self._moving:
            delta = util.vector_mul(util.vector_normalize(self._move_vector),
                                    Camera.MOVE_SPEED * time_passed)
            self.view_rect.move_ip(delta)
            self._post_move_event()

    def set_move(self, x=None, y=None):
        if x is not None:
            self._move_vector[0] = x
        if y is not None:
            self._move_vector[1] = y
        self._moving = True

    def stop_moving(self):
        self._move_vector = [0, 0]
        self._moving = False

    def move_to(self, x, y):
        self.view_rect.x = x
        self.view_rect.y = y
        self._post_move_event()

    def rect_to_screen(self, rect):
        return rect.move(-self.view_rect.x, -self.view_rect.y)

    def rect_to_map(self, rect):
        return rect.move(self.view_rect.x, self.view_rect.y)

    def point_to_screen(self, p):
        return p[0] - self.view_rect.x, p[1] - self.view_rect.y

    def point_to_map(self, p):
        return p[0] + self.view_rect.x, p[1] + self.view_rect.y

    def _post_move_event(self):
        EventManager.post(self.move_event, cam=self)