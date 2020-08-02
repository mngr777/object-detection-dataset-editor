import math

class Shape:
    NAME: "<noname>"

    def data(self):
        raise NotImplementedError

    @staticmethod
    def from_data(data):
        raise NotImplementedError

    def draw(self, canvas):
        canvas.start_shape(self)

    def points(self):
        raise NotImplementedError


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

    @staticmethod
    def from_data(shape, data):
        def error(message):
            raise RuntimeError("Point import: {}".format(message))

        x, y = [data.get("x"), data.get("y")]
        # check coords exist
        if x is None:
            error("`x' field is missing")
        if y is None:
            error("`y' field is missing")
        # check coords are int
        if not isinstance(x, int):
            error("`x' is not int")
        if not isinstance(y, int):
            error("`y' is not int")

        return Point(shape, x, y)
