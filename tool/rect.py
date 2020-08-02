import tool.base as base
import shape as sh

class Rect(base.Tool):
    def __init__(self, context):
        super().__init__(context)
        self.rect = None

    def mousedown(self, event):
        x, y = [event.x, event.y]
        self.rect = sh.Rect(x, y, x, y)
        self.context.add_shape(self.rect)
        self.context.selected = self.rect

    def mouseup(self, event):
        self.rect = None

    def mousemotion(self, event):
        x, y = [event.x, event.y]
        if self.rect:
            points = self.rect.points()
            x_0, y_0 = [points[0].x, points[1].y]
            points[1].moveTo(x, y_0)
            points[2].moveTo(x, y)
            points[3].moveTo(x_0, y)
