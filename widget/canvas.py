import widget.base as base
import tkinter as tk

class Canvas(base.Widget):
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
