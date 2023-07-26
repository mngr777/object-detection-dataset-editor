#!/usr/bin/python
import argparse
import os
import tkinter as tk
import importexport as ie
import sys
import shape
import tool as tl
import widget as wg
from PIL import Image, ImageTk

class Context:
    def __init__(self):
        self.config = {
            "line_width": 1,
            "point_radius": 5,
            "shape_create_min_dist": 10,
            "color_default": "magenta",
            "color_active": "cyan",
            "json_indent": 2
        }
        self.shapes = []
        self.points = []
        self.selected = None
        self.cid = 0
        self.class_labels = []
        self.tool_name = None

        # init tools
        self.tools = {}
        for name, klass in tl.List.items():
            self.tools[name] = klass(self);
        self.select_tool('rect')

    def select_tool(self, name):
        if name in self.tools:
            self.tool_name = name

    def get_tool(self):
        return self.tools[self.tool_name]

    def get_tool_name(self):
        return self.tool_name

    def add_shape(self, shape):
        self.shapes.append(shape)
        self.points.extend(shape.get_points())

    def remove_shape(self, shape):
        self.shapes.remove(shape)
        for p in shape.get_points():
            self.points.remove(p)


def parse_args():
    binding_description = """
Click and drag to create shape.
Click on a shape point to select, drag point to change.

Bindings:
  t               Select next tool.
  d, <Delete>     Delete selected shape.
  <space>         Dump data to file (if --data=filename provided) or print.
  <Return>        Dump data to file (if --data=filename provided) or print and exit.
  <Escape>        Exit.
  <Control>-b     Exit with status 1, signals the wrapping script to (b)reak.
  <Control>-r     Exit with status 2, signals the wrapping script to (r)eturn to previous image.
  [0-9]           Toggle shape class if selected, otherwise set default shape class.
  <Control>-[0-9] Same for classes 10 -- 19.
"""
    parser = argparse.ArgumentParser(
        epilog=binding_description,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("image", help="Image file path")
    parser.add_argument("--data", "-d", help="Data file path")
    parser.add_argument("--tool", "-t", choices=tl.List.keys(), help="Tool")
    parser.add_argument("--labels", "-l", help="Class labels, comma separated")
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
    if args.tool:
        context.select_tool(args.tool)
    if args.labels:
        context.class_labels = args.labels.split(',')

    # load image
    image = Image.open(args.image)
    image_tk = ImageTk.PhotoImage(image)

    # main frame
    content = tk.Frame(root)
    content.grid()

    # canvas
    canvas = wg.Canvas(context, content, image_tk)
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

    # classes
    # NOTE: allows only 20 classes, to use more add some input popup
    def toggle_or_select_default_shape_class(cid):
        def toggle_or_select(_):
            sh = context.selected
            if sh:
                sh.toggle_class(cid)
                canvas.update()
            else:
                context.cid = cid
        return toggle_or_select
    for cid in range(10):
        # 0 -- 9
        root.bind(f'<KP_{cid}>', toggle_or_select_default_shape_class(cid))
        root.bind(f'{cid}', toggle_or_select_default_shape_class(cid))
        # 10 -- 19
        for ctrl in ['<Control_L>', '<Control_R>']:
            root.bind(f'{ctrl}<KP_{cid}>', toggle_or_select_default_shape_class(cid+10))
            root.bind(f'{ctrl}{cid}', toggle_or_select_default_shape_class(cid+10))


    def rect_grow(amount):
        def grow(_):
            sh = context.selected
            if sh and isinstance(sh, shape.Rect):
                sh.grow(amount)
                canvas.update()
        return grow
    root.bind('+', rect_grow(+1))
    root.bind('-', rect_grow(-1))
    root.bind('<KP_Add>', rect_grow(+1))
    root.bind('<KP_Subtract>', rect_grow(-1))

    def next_tool(_):
        names = list(tl.List.keys())
        idx = names.index(context.get_tool_name())
        idx = (idx + 1) % len(names)
        context.select_tool(names[idx])
    root.bind("t", next_tool)

    # export and continue
    def export_data_and_continue(_):
        export_data(context, args.data)
    root.bind("<space>", export_data_and_continue)

    # export and exit
    def export_data_and_exit(_):
        export_data(context, args.data)
        root.destroy()
    root.bind("<Return>", export_data_and_exit)
    root.bind("<KP_Enter>", export_data_and_exit)

    def exit_no_save(_):
        root.destroy()
    root.bind("<Escape>", exit_no_save)

    def exit_break(_):
        sys.exit(1)
    root.bind("<Control_L>b", exit_break)
    root.bind("<Control_R>b", exit_break)

    def exit_return(_):
        sys.exit(2)
    root.bind("<Control_L>r", exit_return)
    root.bind("<Control_R>r", exit_return)

    # loop
    root.mainloop()

if __name__ == "__main__":
    main()
