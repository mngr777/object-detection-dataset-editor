#!/usr/bin/python
import sys
import tkinter as tk
from tkinter import ttk

class Shape:
    def data(self):
        return None

    def draw(self, canvas):
        pass

    def points(self):
        return []


class ShapePoint:
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


class RectShape(Shape):
    def __init__(self, x1, y1, x2, y2):
        self.rect_points = (
            ShapePoint(self, x1, y1),
            ShapePoint(self, x2, y1),
            ShapePoint(self, x2, y2),
            ShapePoint(self, x1, y2))

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


class Context:
    def __init__(self):
        self.shapes = []
        self.points = []
        self.selected = None

    def add_shape(self, shape):
        self.shapes.append(shape)
        self.points.extend(shape.points())

    def remove_shape(self, shape):
        self.shapes.remove(shape)
        for p in shape.points():
            self.points.remove(p)


class Canvas:
    def __init__(self, context, parent, image):
        self.context = context
        # Init canvas
        self.canvas = tk.Canvas(parent, width=image.width(), height=image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image, tags="image")

        # Set click handler
        me = self
        def onclick(event):
            me.click(event)
        self.canvas.bind("<Button-1>", onclick)

    def click(self, event):
        print("Click at ({}, {})".format(event.x, event.y))
        self.__update()

    def __update(self):
        # Reset
        self.canvas.delete("point")
        self.canvas.delete("line")
        # Draw
        for s in self.context.shapes:
            s.draw(self.canvas)

def exit_usage():
    print("Usage: TODO")
    sys.exit(-1)

def main():
    if len(sys.argv) < 2:
        exit_usage()
    image_filename = sys.argv[1]

    # init Tk
    root = tk.Tk()

    # create context
    context = Context()

    # load image
    image = tk.PhotoImage(file=image_filename)

    # main frame
    content = tk.Frame(root)
    content.grid()

    # canvas
    #canvas = tk.Canvas(content, width=image.width(), height=image.height())
    #canvas.grid()
    canvas = Canvas(context, content, image)
    canvas.canvas.grid()

    # loop
    root.mainloop()

if __name__ == "__main__":
    main()
