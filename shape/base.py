class Shape:
    def data(self):
        return None

    def draw(self, canvas):
        pass

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

    def data(self):
        return (self.x, self.y)

    def draw(self, canvas):
        r = 5
        x, y = [self.x, self.y]
        canvas.create_oval(x - r, y - r, x + r, y + r, tags="point")
