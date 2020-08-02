import math
import shape.base as base

class Rect(base.Shape):
    NAME = "rect"

    def __init__(self, x1, y1):
        self.rect_points = (
            base.Point(self, x1, y1),
            base.Point(self, x1, y1),
            base.Point(self, x1, y1),
            base.Point(self, x1, y1))

    def data(self):
        return {"points": list(map(lambda p: p.data(), self.rect_points))}

    @staticmethod
    def from_data(data):
        def error(message):
            raise RuntimeError("Rect import: {}".format(message))

        # check if data is dict
        if not isinstance(data, dict):
            error("data is not dict")

        points = data.get("points")

        # check if present
        if not points:
            error("`points' field is missing")
        # check if list
        if not isinstance(points, list):
            error("`points' field is not a list")
        # check size
        if len(points) != 4:
            error("`points' list size is {} instead of 4".format(len(points)))

        # create object
        rect = Rect(0, 0)
        # update points
        try:
            for i in range(0, 4):
                p = base.Point.from_data(rect, points[i])
                rect.rect_points[i].x = p.x
                rect.rect_points[i].y = p.y
        except RuntimeError as e:
            error(str(e))
        return rect

    def draw(self, canvas):
        super().draw(canvas)
        for i in range(0, 4):
            p_1, p_2 = [self.rect_points[i], self.rect_points[(i + 1) % 4]]
            canvas.draw_point(p_1.x, p_1.y, hilight=(i == 0))
            canvas.draw_line(p_1.x, p_1.y, p_2.x, p_2.y)

    def points(self):
        return self.rect_points
