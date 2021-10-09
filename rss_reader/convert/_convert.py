import json

from pydantic import BaseModel


def to_json(model: BaseModel):
    model = model.json()
    parsed_json = json.loads(model)
    model = json.dumps(parsed_json, indent=4, ensure_ascii=False)
    return model
