import json


def to_json(model):
    model = model.json()
    parsed_json = json.loads(model)
    model = json.dumps(parsed_json, indent=4)
    return model
