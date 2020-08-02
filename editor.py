#!/usr/bin/python
import argparse
import os
import tkinter as tk
import importexport as ie
import tool as tl
import widget as wg

class Context:
    def __init__(self):
        self.config = {
            "line_width": 2,
            "point_radius": 5,
            "shape_create_min_dist": 10,
            "color_default": "magenta",
            "color_active": "cyan"
        }
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Image file path")
    parser.add_argument("--data", help="Data file path")
    return parser.parse_args()


def import_data_if_exists(context, path):
    if path and path != "-" and os.path.isfile(path):
        with open(path, 'r') as f:
            data_json = f.read()
            if len(data_json) > 0:
                ie.import_json(context, data_json)


def export_data(context, path):
    data_json = ie.export_json(context)
    if path and path != "-":
        with open(path, "w+") as f:
            f.write(data_json)
    else:
        print(data_json)


def main():
    args = parse_args()

    # init Tk
    root = tk.Tk()

    # create context
    context = Context()

    # load image
    image = tk.PhotoImage(file=args.image)

    # main frame
    content = tk.Frame(root)
    content.grid()

    # canvas
    canvas = wg.Canvas(context, content, image)
    canvas.canvas.grid()

    # read data
    if args.data:
        import_data_if_exists(context, args.data)
        canvas.update()

    # shape deletion
    def delete_shape(_):
        sh = context.selected
        if sh:
            context.selected = None
            context.remove_shape(sh)
            canvas.update()
    root.bind("<Delete>", delete_shape)
    root.bind("d", delete_shape)

    # export and continue
    def export_data_and_continue(_):
        export_data(context, args.data)
    root.bind("<space>", export_data_and_continue)

    # export and exit
    def export_data_and_exit(_):
        export_data(context, args.data)
        root.destroy()
    root.bind("<Return>", export_data_and_exit)

    def exit_no_save(_):
        root.destroy()
    root.bind("<Escape>", exit_no_save)

    # loop
    root.mainloop()

if __name__ == "__main__":
    main()
