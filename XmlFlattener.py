import xmltodict


def flatten_xml(d, parent_key='', sep='.'):
    """
    Flatten a nested dictionary by joining keys with a separator.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_xml(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                new_item_key = f"{new_key}[{i}]"
                if isinstance(item, dict):
                    items.extend(flatten_xml(item, new_item_key, sep=sep).items())
                else:
                    items.append((f"{new_item_key}", item))
        else:
            items.append((new_key, v))
    return dict(items)


# Replace 'input.xml' with the path to your XML file
with open('XML_Content.xml', 'r') as f:
    xml_str = f.read()

# Parse the XML string to a nested dictionary
xml_dict = xmltodict.parse(xml_str)

# Flatten the dictionary using '_' as the separator
flat_dict = flatten_xml(xml_dict)

# Print the flattened dictionary
# print(flat_dict)

for k, v in flat_dict.items():
    print(f"\"{k}.text()\", isA(String.class),")
