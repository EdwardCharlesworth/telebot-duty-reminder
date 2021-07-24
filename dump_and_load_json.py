import json
from config import default_dump_path


def dump_dutys(dutys, filepath=default_dump_path):
    with open(filepath,"w") as file:
        file.write(json.dumps([duty.__dict__ for duty in dutys]))


def load_dutys(filepath=default_dump_path):
    try:
        with open(filepath) as f:
            dutys = json.load(f)
        return dutys
    except FileNotFoundError:
        return []
