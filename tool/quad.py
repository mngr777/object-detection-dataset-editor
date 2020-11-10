import tool.base as base
import shape as sh

class Quad(base.Tool):
    NAME = 'quad'

    def __init__(self, context):
        super().__init__(context)
        self.quad = None
        self.max_dist = 0

    def mousedown(self, event):
        x, y = [event.x, event.y]
        self.quad = sh.Quad(x, y)
        self.context.add_shape(self.quad)
        self.context.selected = self.quad

    def mouseup(self, event):
        context = self.context
        if self.max_dist < context.config['shape_create_min_dist']:
            context.remove_shape(self.quad)
            context.selected = None
        self.quad = None
        self.max_dist = 0

    def mousemotion(self, event):
        x, y = [event.x, event.y]
        points = self.quad.get_points()
        x_0, y_0 = [points[0].x, points[1].y]
        points[1].moveTo(x, y_0)
        points[2].moveTo(x, y)
        points[3].moveTo(x_0, y)
        self.max_dist = max(self.max_dist, points[0].dist(points[2]))
