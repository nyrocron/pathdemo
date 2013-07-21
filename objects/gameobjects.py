# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""gameobjects.py: game objects"""

from util import point_dist


class GameObject:
    """Superclass of all game objects, has id and bbox (location) attribute"""

    _id_counter = 0
    MOVE_THRESHOLD = 0.1

    def __init__(self, bbox, obj_id=None):
        self.bbox = bbox
        if obj_id is None:
            self.id = GameObject._new_id()
        else:
            self.id = obj_id

        self.selected = False
        self.max_speed = 2

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

    def update(self, gametime):
        # TODO: move
        pass

    def set_dest(self, x, y):
        if point_dist((x, y), self.bbox.center) > GameObject.MOVE_THRESHOLD:
            # TODO: update dest
            pass

    @staticmethod
    def _new_id():
        GameObject._id_counter += 1
        return GameObject._id_counter


class Unit(GameObject):
    pass