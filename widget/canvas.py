import math
import tkinter as tk
import widget.base as base

class Canvas(base.Widget):
    def __init__(self, context, parent, image):
        self.context = context
        # Init canvas
        self.canvas = tk.Canvas(parent, width=image.width(), height=image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image, tags="image")
        self.color = self.context.config['color_default']

        me = self
        # mousedown
        def mousedown(event):
            me.mousedown(event)
        self.canvas.bind("<Button-1>", mousedown)
        # mouseup
        def mouseup(event):
            me.mouseup(event)
        self.canvas.bind("<ButtonRelease-1>", mouseup)
        # mousemotion
        def mousemotion(event):
            me.mousemotion(event)
        self.canvas.bind("<B1-Motion>", mousemotion)

        self.dragged_point = None

    def mousedown(self, event):
        p = self.__find_point_at(event.x, event.y)
        t = self.context.get_tool()
        if p:
            self.dragged_point = p
            self.context.selected = p.shape
        elif t:
            t.mousedown(event)
        self.update()

    def mouseup(self, event):
        p = self.dragged_point
        t = self.context.get_tool()
        if p:
            self.dragged_point = None
        elif t:
            t.mouseup(event)
        self.update()

    def mousemotion(self, event):
        p = self.dragged_point
        t = self.context.get_tool()
        if p:
            p.moveTo(event.x, event.y)
        elif t:
            t.mousemotion(event)
        self.update()

    def update(self):
        # Reset
        self.canvas.delete("point")
        self.canvas.delete("line")
        # Draw
        for s in self.context.shapes:
            s.draw(self)

    def start_shape(self, shape):
        config = self.context.config
        if shape is self.context.selected:
            self.color = config['color_active']
        else:
            self.color = config['color_default']

    def end_shape(self, shape):
        pass

    def draw_line(self, x1, y1, x2, y2):
        w = self.context.config['line_width']
        self.canvas.create_line(x1, y1, x2, y2, tags="line", fill=self.color, width=w)

    def draw_point(self, x, y, hilight=False):
        w = self.context.config['line_width']
        r = self.context.config['point_radius']
        self.canvas.create_oval(x - r, y - r, x + r, y + r, tags="point", outline=self.color, width=w)
        if hilight:
            r += (w * 1.5)
            self.canvas.create_oval(x - r, y - r, x + r, y + r, tags="point", outline=self.color, width=w)

    def draw_rect(self, x, y, width, height):
        w = self.context.config['line_width']
        self.canvas.create_rectangle(x, y, x + width, y + height, tags="line", outline=self.color, width=w)

    def __find_point_at(self, x, y):
        r = self.context.config['point_radius']
        for p in self.context.points:
            d = math.sqrt((p.x - x)**2 + (p.y - y)**2)
            if d <= r:
                return p
        return None
