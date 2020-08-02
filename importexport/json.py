import json
import shape as sh

def import_json(context):
    return []

def export_json(context):
    data = list(map(lambda s: {"type": type(s).__name__, "data": s.data()}, context.shapes))
    return json.dumps(data)
