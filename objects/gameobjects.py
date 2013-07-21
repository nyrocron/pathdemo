# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""gameobjects.py: game objects"""

import util


class GameObject:
    """Superclass of all game objects, has id and bbox (location) attribute"""

    _id_counter = 0

    def __init__(self, manager, bbox):
        self._manager = manager
        self.bbox = bbox
        self.id = GameObject._new_id()

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

    def __init__(self, manager, bbox):
        GameObject.__init__(self, manager, bbox)
        self._waypoints = []
        self._is_moving = False

        self.speed = 0.1

    def update(self, gametime):
        if self._is_moving:
            if gametime > self._move_end_time:
                self._is_moving = False
            else:
                time_passed = gametime - self._move_start_time
                new_pos = util.vector_add(self._move_start,
                                          util.vector_mul(self._move_dir,
                                          time_passed * self.speed))
                self._manager.move_object_to(self, new_pos)
        else:
            if len(self._waypoints) > 0:
                self._move_start_time = gametime
                move_dist = self._set_dest(self._waypoints.pop(0))
                self._move_end_time = gametime + move_dist / self.speed

    def send_to(self, destination):
        center_dst = (destination[0] - self.bbox.width / 2,
                      destination[1] - self.bbox.height / 2)
        self._waypoints = [center_dst]

    def _set_dest(self, dst):
        pos = (self.bbox.x, self.bbox.y)
        if util.point_dist(dst, pos) > Unit.MOVE_THRESHOLD:
            move_vector = util.vector_diff(dst, pos)
            self._move_start = pos
            self._move_dir = util.vector_normalize(move_vector)
            self._is_moving = True
            return util.vector_len(move_vector)
        else:
            return 0