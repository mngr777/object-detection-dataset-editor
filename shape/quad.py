import math
import shape.base as base

class Quad(base.Shape):
    NAME = "quad"

    def __init__(self, x1, y1):
        super().__init__()
        self.points = (
            base.Point(self, x1, y1),
            base.Point(self, x1, y1),
            base.Point(self, x1, y1),
            base.Point(self, x1, y1))

    def get_data(self):
        return {
            "classes": self.get_classes(),
            "points": [p.get_data() for p in self.points]}

    @staticmethod
    def from_data(data):
        def error(message):
            raise RuntimeError("Quad import: {}".format(message))

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
        quad = Quad(0, 0)
        # update points
        try:
            for i in range(0, 4):
                p = base.Point.from_data(quad, points[i])
                quad.points[i].x = p.x
                quad.points[i].y = p.y
        except RuntimeError as e:
            error(str(e))

        # classes
        quad.add_classes(data.get("classes", [0]))

        return quad

    def do_draw(self, canvas):
        for i in range(0, 4):
            p_1, p_2 = [self.points[i], self.points[(i + 1) % 4]]
            canvas.draw_point(p_1.x, p_1.y, hilight=(i == 0))
            canvas.draw_line(p_1.x, p_1.y, p_2.x, p_2.y)
        class_text = ', '.join(self.get_class_names(canvas.context.class_labels))
        canvas.draw_text(self.points[0].x, self.points[0].y - 14, class_text)

    def get_points(self):
        return self.points
