import copy
import math

class Shape:
    NAME = "<noname>"

    def __init__(self):
        self.classes = set()

    def get_data(self):
        raise NotImplementedError

    @staticmethod
    def from_data(data):
        raise NotImplementedError

    def draw(self, canvas):
        self.before_draw(canvas)
        self.do_draw(canvas)
        self.after_draw(canvas)

    def before_draw(self, canvas):
        canvas.start_shape(self)

    def do_draw(self, canvas):
        pass

    def after_draw(self, canvas):
        canvas.end_shape(self)

    def get_points(self):
        raise NotImplementedError

    def get_classes(self):
        return sorted(self.classes)

    def get_class_names(self, labels=[]):
        return [labels[cid] if cid < len(labels) else str(cid) for cid in self.get_classes()]

    def add_classes(self, cids):
        for cid in cids:
            if not isinstance(cid, int):
                raise ValueError(f'Class index is not integer: {cid}')
            self.add_class(cid)

    def add_class(self, cid):
        self.classes.add(cid)

    def remove_class(self, cid):
        self.classes.discard(cid)

    def toggle_class(self, cid):
        self.remove_class(cid) if cid in self.classes else self.add_class(cid)


class Point:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.moveTo(x, y)

    def move(self, x, y):
        self.moveTo(self.x + x, self.y + y)

    def moved(self, x, y):
        cp = copy.copy(self)
        cp.move(x, y)
        return cp

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def get_data(self):
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
