# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""management.py: game object management"""

from pygame import Rect


class TreeError(Exception):
    pass


class QuadtreeNode(object):
    """Represents one noe of a Quadtree."""

    def __init__(self, parent, bbox):
        """Create new Quadtree node."""
        if (not self._is_power2(bbox.width) or not
                self._is_power2(bbox.height)):
            raise TreeError("node dimensions have to be power of two,"
                            " bbox given was " + str(bbox))

        assert(parent is None or isinstance(parent, QuadtreeNode))
        self.parent = parent
        self._bb = bbox

        self._data = set()
        self._has_children = False
        self._childs = [None] * 4

    def insert(self, obj):
        """Insert object into the tree under this node."""
        if not self._bb.contains(obj.bbox):
            return False

        if not self._has_children:
            self._subdivide()

        if self._has_children:
            for child in self._childs:
                if child.insert(obj):
                    return True

        self._data.add(obj)
        return True

    def query_at(self, point):
        result = set()
        if not self._bb.collidepoint(point):
            return result

        if len(self._data) > 0:
            for obj in self._data:
                if obj.bbox.collidepoint(point):
                    result.add(obj)

        if self._has_children:
            for child in self._childs:
                result.update(child.query_at(point))

        return result

    def query(self, area=None):
        """Query for objects in the tree under this node.

        If area is set this will only objects that are contained in area"""
        result = set()
        if area is not None and not self._bb.contains_rect(area):
            return result

        if len(self._data) > 0:
            for obj in self._data:
                if area is None or area.contains_rect(obj.bbox):
                    result.add(obj)

        if self._has_children:
            for child in self._childs:
                result.update(child.query(area))

        return result

    def query_intersect(self, area):
        """Query for objects in the tree under this node.

        If area is set this will only objects that intersect with area"""
        result = set()
        if not self._bb.colliderect(area):
            return result

        if len(self._data) > 0:
            for obj in self._data:
                if obj.bbox.colliderect(area):
                    result.add(obj)

        if not self._has_children:
            return result

        for child in self._childs:
            result.update(child.query_intersect(area))

        return result

    def move_to(self, obj, new_bbox):
        """Move obj to new location."""
        if not self._bb.contains(obj.bbox):
            return False
        if obj in self._data:
            self._data.remove(obj)
            obj.bbox = new_bbox
            self._insert_up(obj)
            return True
        for child in self._childs:
            if child.move_to(obj, new_bbox):
                return True
        raise TreeError("move failed")

    def print_tree(self, indent=0):
        """Print contents of this tree"""
        print(' ' * indent + str(self._data))

        if not self._has_children:
            return

        for child in self._childs:
            child.print_tree(indent + 2)

    def _insert_up(self, obj):
        if self._bb.contains(obj.bbox):
            self.insert(obj)
        else:
            self.parent._insert_up(obj)

    def _subdivide(self):
        split_width = self._bb.width // 2
        split_height = self._bb.height // 2
        split_x = self._bb.x + split_width
        split_y = self._bb.y + split_height

        if split_width == 0 or split_height == 0:
            return False

        self._childs[0] = QuadtreeNode(self, Rect(self._bb.x, self._bb.y,
                                                  split_width, split_height))
        self._childs[1] = QuadtreeNode(self, Rect(split_x, self._bb.y,
                                                  split_width, split_height))
        self._childs[2] = QuadtreeNode(self, Rect(self._bb.x, split_y,
                                                  split_width, split_height))
        self._childs[3] = QuadtreeNode(self, Rect(split_x, split_y,
                                                  split_width, split_height))

        self._has_children = True
        return True

    def _has_data(self):
        return len(self._data) > 0

    def _purge_empty_nodes(self):
        if self._has_data():
            return

        if self._has_children:
            for child in self._childs:
                if child._has_children or child._has_data():
                    return

        self._childs = [None] * 4
        self._has_children = False
        if self.parent is not None:
            self.parent._purge_empty_nodes()

    def _is_power2(self, n):
        return ((n & (n - 1)) == 0) and n > 0


class Quadtree(QuadtreeNode):
    """Represents a quadtree that contains objects with a location attribute"""

    def __init__(self, bbox):
        QuadtreeNode.__init__(self, None, bbox)


class ObjectManagementError(Exception):
    pass


class ObjectManager(object):
    """Manages game objects and provides methods for interacting with them"""

    def __init__(self, bbox):
        self._bb = bbox
        self._quadtree = Quadtree(self._bb)
        self._id_to_obj = {}
        self.selection = set()

    def update(self, gametime):
        """Update objects"""
        for obj in self._id_to_obj.values():
            obj.update(gametime)

    def create(self, which, location):
        """Create a new object of type which at location."""
        obj = which(self, location)
        self._id_to_obj[obj.id] = obj
        self._quadtree.insert(obj)
        return obj

    def query(self, location=None, point=None):
        """Get all objects or all objects that intersect with area if set."""
        if point is not None:
            return self._quadtree.query_at(point)
        return self._quadtree.query_intersect(location)

    def get_object_by_id(self, obj_id):
        """Get an object by its id."""
        return self._id_to_obj[obj_id]

    def move_object(self, obj_id, x, y):
        """Move object with id obj_id by (x, y)."""
        obj = self.get_object_by_id(obj_id)
        new_bbox = obj.bbox.move(x, y)
        if not self._bb.contains(new_bbox):
            return False
        self._quadtree.move_to(obj, new_bbox)
        return True

    def move_object_to(self, obj, pos):
        """Move object to new position."""
        new_bbox = Rect(pos, obj.bbox.size)
        if not self._bb.contains(new_bbox):
            return False
        self._quadtree.move_to(obj, new_bbox)
        return True

    def select_area(self, area):
        """Select all objects whose bbox collides with area."""
        self.select_objects(self._quadtree.query_intersect(area))

    def select_at(self, point):
        """Select all objects whose bbox collides with point."""
        self.select_objects(self._quadtree.query_at(point))

    def select_objects(self, objs):
        for obj in self.selection.difference(objs):
            obj.selected = False

        self.selection = objs
        for obj in self.selection:
            obj.selected = True

    def send_selected(self, destination, add_waypoint=False):
        """Send all selected objects to (x, y)."""
        for obj in self.selection:
            obj.send_to(destination, add_waypoint)