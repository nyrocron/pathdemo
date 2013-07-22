# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""camera.py: camera management"""

from pygame import Rect
from events import EventManager


class Camera:
    """Manages current view rectangle and provides methods to convert
    coordinates from/to screen/map coordinate systems."""

    def __init__(self, view_size):
        self.view_rect = Rect((0, 0), view_size)
        self.move_event = EventManager.new_event_code()

    def move(self, x, y):
        self.view_rect = self.view_rect.move(x, y)
        EventManager.post(self.move_event)

    def rect_to_screen(self, rect):
        return rect.move(-self.view_rect.x, -self.view_rect.y)

    def rect_to_map(self, rect):
        return rect.move(self.view_rect.x, self.view_rect.y)

    def point_to_screen(self, x, y):
        return x - self.view_rect.x, y - self.view_rect.y

    def point_to_map(self, x, y):
        return x + self.view_rect.x, y + self.view_rect.y