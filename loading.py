"""loading functions"""

from item import Item
import json


def load_items(file_path: str) -> dict[int, set[Item]]:
    """
    loads items from file_path

    Preconditions:
    file_path leads to .json
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    output = {5: set(), 4: set(), 3: set()}

    for star in data:
        for name in data[star]:
            item = Item(name, star)
            output[star].add(item)

    return output
