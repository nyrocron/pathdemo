__author__ = 'flori_000'


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.right = self.x + self.width
        self.bottom = self.y + self.height

    def __str__(self):
        return ('Rectangle(' + str(self.x) + ', ' + str(self.y) + ', ' +
                str(self.width) + ', ' + str(self.height) + ')')

    def get_center(self):
        return self.x + self.width // 2, self.y + self.height // 2

    def contains_point(self, x, y):
        return (x >= self.x and y >= self.y and
                x <= self.x + self.width and
                y <= self.y + self.height)

    def contains_rect(self, other):
        return (other.x >= self.x and other.right <= self.right and
                other.y >= self.y and other.bottom <= self.bottom)

    def intersects(self, other):
        separate = (self.x + self.width < other.x or
                    self.y + self.height < other.y or
                    self.x > other.x + other.width or
                    self.y > other.y + other.height)
        return not separate