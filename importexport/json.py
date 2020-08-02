import json
import shape as sh

def import_json(context, data_json):
    def error(message):
        raise RuntimeError("Import: {}".format(message));

    data = json.loads(data_json)
    if not isinstance(data, list):
        error("data is not a list")
    for item in data:
        # get shape class by type
        t = item.get("type")
        shape_class = sh.ShapeList.get(t)
        if not shape_class:
            error("invalid shape type `{}'".format(t))
        # make shape from data
        s = shape_class.from_data(item.get("data"))
        context.add_shape(s)


def export_json(context):
    data = list(map(lambda s: {"type": type(s).NAME, "data": s.data()}, context.shapes))
    return json.dumps(data)
