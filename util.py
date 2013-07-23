# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""util.py: """

from math import sqrt
from pygame import Rect


class HashRect(Rect):
    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))


def point_dist(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def vector_normalize(v):
    vlen = sqrt(v[0] ** 2 + v[1] ** 2)
    return v[0] / vlen, v[1] / vlen


def vector_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def vector_diff(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def vector_mul(v, n):
    return v[0] * n, v[1] * n


def vector_len(v):
    return sqrt(v[0] ** 2 + v[1] ** 2)