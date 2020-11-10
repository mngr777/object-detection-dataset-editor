import tool.base as base
import shape as sh

class Rect(base.Tool):
    NAME = 'rect'

    def __init__(self, context):
        super().__init__(context)
        self.rect = None
        self.max_dist = 0

    def mousedown(self, event):
        x, y = [event.x, event.y]
        self.rect = sh.Rect(x, y);
        self.context.add_shape(self.rect)
        self.context.selected = self.rect

    def mouseup(self, event):
        context = self.context
        if self.max_dist < context.config['shape_create_min_dist']:
            context.remove_shape(self.rect)
            context.selected = None
        self.rect = None
        self.max_dist = 0

    def mousemotion(self, event):
        x, y = [event.x, event.y]
        points = self.rect.get_points()
        points[1].moveTo(x, y)
        self.max_dist = max(self.max_dist, points[0].dist(points[1]))
