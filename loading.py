"""loading functions"""

from item import Item
import json
import os
from player_classes import Inventory, Player, PlayerPity
from pity import StandardPity, LimitedPity, LightConePity

PLAYER_DATA_FOLDER_FILE_PATH = 'json/player_data/'

# file_name would be f'{PLAYER_DATA_NAME_TEMPLATE}_{id}.json'
PLAYER_DATA_NAME_TEMPLATE = 'player_id_'


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
            item = Item(name, int(star), data[star][name])
            output[int(star)].append(item)

    return output


def load_player_data(id: str) -> Player:
    """
    loads players from file_path

    Preconditions:
    file_path leads to .json
    """
    file_path = find_file(f'{PLAYER_DATA_NAME_TEMPLATE}{id}.json', PLAYER_DATA_FOLDER_FILE_PATH)
    if file_path is not None:
        with open(file_path, 'r') as file:
            data = json.load(file)

        inventory, pity = data[str(id)]

        new_inventory = Inventory({int(star): inventory[star] for star in inventory})

        standard_pity, limited_pity, light_cone_pity = (pity['standard_pity'], pity['limited_pity'],
                                                        pity['light_cone_pity'])

        standard = StandardPity(standard_pity[0], standard_pity[1])
        limited = LimitedPity(limited_pity[0], limited_pity[1], limited_pity[2])
        light_cone = LightConePity(light_cone_pity[0], light_cone_pity[1], light_cone_pity[2])

        new_pity = PlayerPity(standard, limited, light_cone)

        return Player(id, new_inventory, new_pity)

    raise ValueError


def find_file(filename, search_path):
    """look for filename in search_path"""
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)

    return None
