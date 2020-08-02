#!/usr/bin/python
import sys
import tkinter as tk
from tkinter import ttk
import tool as tl
import widget as wg

class Context:
    def __init__(self):
        self.shapes = []
        self.points = []
        self.selected = None
        self.tool = None
        self.tool = tl.Rect(self)

    def set_tool(self, tool):
        self.tool = tool

    def get_tool(self):
        return self.tool

    def add_shape(self, shape):
        self.shapes.append(shape)
        self.points.extend(shape.points())

    def remove_shape(self, shape):
        self.shapes.remove(shape)
        for p in shape.points():
            self.points.remove(p)


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
    canvas = wg.Canvas(context, content, image)
    canvas.canvas.grid()

    # loop
    root.mainloop()

if __name__ == "__main__":
    main()
