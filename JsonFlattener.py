import json


def flatten_json(json_obj, prefix=''):
    """
    Flatten a JSON object by combining nested keys into a single key separated by dots.
    """
    flattened = {}
    for key, value in json_obj.items():
        new_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened.update(flatten_json(item, f"{new_key}[{i}]"))
                else:
                    flattened[f"{new_key}[{i}]"] = item
        else:
            flattened[new_key] = value
    return flattened


with open('JSON_Content.json', 'r') as f:
    json_str = f.read()

json_obj = json.loads(json_str)

# Flatten the JSON object
flattened_json = flatten_json(json_obj)

# Print the flattened JSON for debugging purposes
# print(json.dumps(flattened_json, indent=2))
# print(flattened_json)

for k, v in flattened_json.items():
    print(f"\"{k}\", ")
