"""loading functions"""
from banner import LightConeBanner, LimitedBanner, Banner
from item import Item
import json
import os

from player_classes import Inventory, Player, PlayerPity
from pity import StandardPity, LimitedPity, LightConePity

from constants import (PLAYER_DATA_FOLDER_FILE_PATH, PLAYER_DATA_NAME_TEMPLATE,
                       STANDARD_BANNER_FILE_PATH, LIMITED_BANNER_FILE_PATH,
                       LIGHT_CONE_FILE_PATH, RATE_UP_FILE_PATH)


def _load_items(file_path: str) -> dict[int, list[Item]]:
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


def load_rate_up(file_path: str) -> dict:
    """loads items from file_path"""
    with open(file_path, 'r') as file:
        data = json.load(file)

    output = {}

    for version in data:
        output[version] = {}
        for banner in data[version]:
            dict = {5: [], 4: []}
            for star in data[version][banner]:
                for name in data[version][banner][star]:
                    if banner == 'limited':
                        type = 'character'
                    else:
                        type = 'light cone'
                    item = Item(name, int(star),  type)
                    dict[int(star)].append(item)
            output[version][banner] = dict

    return output


def load_standard_banner(pity: StandardPity) -> Banner:
    """loads standard banner"""
    standard_loot_pool = _load_items(STANDARD_BANNER_FILE_PATH)
    return Banner(standard_loot_pool, pity)


def load_limited_banner(pity: LimitedPity, version: str = '1.0.1') -> LimitedBanner:
    """loads limited banner"""
    rate_up = load_rate_up(RATE_UP_FILE_PATH)
    loot_pool = _load_items(LIMITED_BANNER_FILE_PATH)

    five_star_rate_up = rate_up[version]['limited'][5][0]
    four_star_rate_up = rate_up[version]['limited'][4]

    return LimitedBanner(loot_pool, five_star_rate_up, four_star_rate_up, pity)


def load_light_cone_banner(pity: LightConePity, version: str = '1.0.1') -> LightConeBanner:
    """loads light cone banner"""
    rate_up = load_rate_up(RATE_UP_FILE_PATH)
    loot_pool = _load_items(LIGHT_CONE_FILE_PATH)

    five_star_rate_up = rate_up[version]['light cone'][5][0]
    four_star_rate_up = rate_up[version]['light cone'][4]

    return LightConeBanner(loot_pool, five_star_rate_up, four_star_rate_up, pity)


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
