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
        super().draw(canvas)
        for i in range(0, 4):
            p_1, p_2 = [self.rect_points[i], self.rect_points[(i + 1) % 4]]
            canvas.draw_point(p_1.x, p_1.y, hilight=(i == 0))
            canvas.draw_line(p_1.x, p_1.y, p_2.x, p_2.y)

    def points(self):
        return self.rect_points
