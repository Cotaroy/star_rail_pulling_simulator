"""loading functions"""

from item import Item
import json


def load_items(file_path: str) -> dict[int, list[Item]]:
    """
    loads items from file_path

    Preconditions:
    file_path leads to .json
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    output = {5: [], 4: [], 3: []}

    for star in data:
        for name in data[star]:
            item = Item(name, int(star))
            output[int(star)].append(item)

    return output
