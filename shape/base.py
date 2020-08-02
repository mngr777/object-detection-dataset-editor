import math

class Shape:
    def data(self):
        return None

    def draw(self, canvas):
        canvas.start_shape(self)

    def points(self):
        return []


class Point:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.moveTo(x, y)

    def move(self, x, y):
        self.moveTo(self.x + x, self.y + y)

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def data(self):
        return {"x": self.x, "y": self.y}
