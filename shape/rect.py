import shape.base as base

class Rect(base.Shape):
    def __init__(self, x1, y1, x2, y2):
        self.rect_points = (
            base.Point(self, x1, y1),
            base.Point(self, x2, y1),
            base.Point(self, x2, y2),
            base.Point(self, x1, y2))

    def data(self):
        return tuple(map(lambda p: p.data(), self.rect_points))

    def draw(self, canvas):
        for i in range(0, 4):
            p1, p2 = [self.rect_points[i], self.rect_points[(i + 1) % 4]]
            p1.draw(canvas)
            p2.draw(canvas)
            canvas.create_line(p1.x, p1.y, p2.x, p2.y, tags="line")

    def points(self):
        return self.rect_points;
