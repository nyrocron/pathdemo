# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""gameobjects.py: game objects"""

import util


class GameObject:
    """Superclass of all game objects, has id and bbox (location) attribute"""

    _id_counter = 0

    def __init__(self, manager, bbox, obj_id=None):
        self._manager = manager
        self.bbox = bbox
        if obj_id is None:
            self.id = GameObject._new_id()
        else:
            self.id = obj_id

        self.selected = False

    def __repr__(self):
        return '<' + str(self) + '>'

    def __str__(self):
        return ('GameObject(' + str(self.bbox) + ', id=' + str(self.id) + ')')

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other

    def __getattr__(self, item):
        if item == 'size':
            return self.bbox.width, self.bbox.height

    @staticmethod
    def _new_id():
        GameObject._id_counter += 1
        return GameObject._id_counter


class Unit(GameObject):
    MOVE_THRESHOLD = 0.5

    def __init__(self, manager, bbox, obj_id=None):
        GameObject.__init__(self, manager, bbox, obj_id)
        self._waypoints = []
        self._is_moving = False

        self.speed = 0.1

    def update(self, time_passed):
        if self._is_moving:
            pos = (self.bbox.x, self.bbox.y)
            if util.point_dist(pos, self._destination) < Unit.MOVE_THRESHOLD:
                self._is_moving = False
            else:
                move_dist = self.speed * time_passed
                move_dir = util.vector_normalize(
                    util.vector_diff(self._destination, pos))
                move_x, move_y = util.vector_mul(move_dir, move_dist)
                self._manager.move_object(self.id, move_x, move_y)
        else:
            if len(self._waypoints) > 0:
                self._set_dest(self._waypoints.pop(0))

    def send_to(self, destination):
        self._waypoints = [destination]

    def _set_dest(self, dst):
        pos = (self.bbox.x, self.bbox.y)
        if util.point_dist(dst, pos) > Unit.MOVE_THRESHOLD:
            self._destination = dst
            self._is_moving = True