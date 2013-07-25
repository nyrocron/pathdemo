# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""pathfinding.py: """


class Pathfinder(object):
    def __init__(self, size_x, size_y):
        self._size_x = size_x
        self._size_y = size_y

    def find_path(self, from_coords, to_coords):
        pass