import math
import shape.base as base

class Rect(base.Shape):
    NAME = "rect"

    def __init__(self, x1, y1, width = 0, height = 0):
        super().__init__()
        p_1 = base.Point(self, x1, y1)
        self.points = (p_1, p_1.moved(width, height))

    def get_data(self):
        p_1, p_2 = self.points
        x_min = min(p_1.x, p_2.x)
        x_max = max(p_1.x, p_2.x)
        y_min = min(p_1.y, p_2.y)
        y_max = max(p_1.y, p_2.y)
        return {
            "classes": self.get_classes(),
            "x": x_min,
            "y": y_min,
            "w": x_max - x_min,
            "h": y_max - y_min
        }

    @staticmethod
    def from_data(data):
        def error(message):
            raise RuntimeError("Rect import: {}".format(message))

        def check_int_field(data, field):
            if field not in data:
                error("`{}' is missing".format(field))
            if not isinstance(data[field], int):
                error("`{}' is not int: `{}'".format(field, data[field]))

        # check if data is dict
        if not isinstance(data, dict):
            error("data is not dict")

        # check values
        check_int_field(data, "x")
        check_int_field(data, "y")
        check_int_field(data, "w")
        check_int_field(data, "h")

        # create object
        rect = Rect(data["x"], data["y"], data["w"], data["h"])

        # classes
        rect.add_classes(data.get("classes", [0]))

        return rect

    def grow(self, amount):
        self.points[0].move(-amount, -amount)
        self.points[1].move(amount, amount)

    def do_draw(self, canvas):
        data = self.get_data()
        canvas.draw_rect(data["x"], data["y"], data["w"], data["h"])
        p_1, p_2 = self.points
        canvas.draw_point(p_1.x, p_1.y)
        canvas.draw_point(p_2.x, p_2.y)
        class_text = ', '.join(self.get_class_names(canvas.context.class_labels))
        canvas.draw_text(data["x"], data["y"] - 10, class_text)

    def get_points(self):
        return self.points;
