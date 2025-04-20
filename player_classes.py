"""player classes"""

from __future__ import annotations

import json

from item import Item
from pity import StandardPity, LightConePity, LimitedPity
from banner import Banner

from constants import PLAYER_DATA_FOLDER_FILE_PATH


class Player:
    """
    player class

    Instance Attributes
    - id: the player ID
    - _inventory: dictionary {item_name: number of that item}
    - _pity: how many pulls since last five star
    """
    id: int
    _inventory: Inventory
    pity: PlayerPity

    def __init__(self, id, inv=None, pity=None):
        if inv is None:
            inv = Inventory()
        if pity is None:
            pity = PlayerPity()

        self.id = id
        self._inventory = inv
        self.pity = pity

    def show_inventory(self):
        """show inventory"""
        print(self._inventory)

    def show_pity(self):
        """show pity"""
        print(self.pity)

    def pull(self, n: int, banner: Banner):
        """
        do n number of pulls
        mutates inventory
        mutates pity

        Preconditions:
        self.pity.{whatever pity} == banner.pity
        """
        for _ in range(n):
            item = banner.pull()
            self._inventory.add_to_inventory(item)
            print(f'[{banner.pity.five_star_pity}] \t You got {str(item)}')

    def save(self):
        """
        save player data to file_path_player_id_{id}

        file_path should just be the path to the foler that all player data files will be stored in
        """
        inv = self._inventory.to_dict()
        pity = self.pity.to_dict()

        dct = {self.id: [inv, pity]}

        with open(PLAYER_DATA_FOLDER_FILE_PATH + f'player_id_{self.id}.json', 'w') as file:
            json.dump(dct, file, **{'indent': 4})


class Inventory:
    """
    inventory of items

    items: [star: dict[Item, number of that Item]]
    """
    items: dict[int, [dict[str, int], dict[str, int], dict[str, int]]] | dict[int: dict]

    def __init__(self, items=None):
        if items is None:
            items = {5: {}, 4: {}, 3: {}}
        self.items = items

    def __str__(self):
        five_stars = ''
        for item in self.items[5]:
            five_stars += f'||| \t {self.items[5][item]}\t\t:\t\t{item}\n'

        four_stars = ''
        for item in self.items[4]:
            four_stars += f'||| \t {self.items[4][item]}\t\t:\t\t{item}\n'

        three_stars = ''
        for item in self.items[3]:
            three_stars += f'||| \t {self.items[3][item]}\t\t:\t\t{item}\n'

        build = (f'---------------------\n'
                 f'5 STARS:\n'
                 f'{five_stars}'
                 f'---------------------\n'
                 f'4 STARS\n'
                 f'{four_stars}'
                 f'---------------------\n'
                 f'3 STARS\n'
                 f'{three_stars}'
                 f'---------------------\n')
        return build

    def add_to_inventory(self, item: Item):
        """add item to inventory"""
        self._add_to_inventory(item, item.star)

    def _add_to_inventory(self, item, star):
        """helper"""
        if item.name not in self.items[star]:
            self.items[star][item.name] = 1
        else:
            self.items[star][item.name] += 1

    def to_dict(self):
        """to dict"""
        return self.items


class PlayerPity:
    """tracks the three types of pity"""
    standard_pity: StandardPity
    limited_pity: LimitedPity
    light_cone_pity: LightConePity

    def __init__(self, standard=None, limited=None, lc=None):
        if standard is None:
            standard = StandardPity()
        if limited is None:
            limited = LimitedPity()
        if lc is None:
            lc = LightConePity()
        self.standard_pity = standard
        self.limited_pity = limited
        self.light_cone_pity = lc

    def __str__(self):
        build = (f'---------------------\n'
                 f'Limited Pity: \t\t{str(self.limited_pity)}\n'
                 f'Light Cone Pity: \t{str(self.light_cone_pity)}\n'
                 f'Standard Pity: \t\t{str(self.standard_pity)}\n'
                 f'---------------------\n')
        return build

    def to_dict(self):
        """to dict"""
        dct = {"standard_pity": self.standard_pity.to_list(),
               "limited_pity": self.limited_pity.to_list(),
               "light_cone_pity": self.light_cone_pity.to_list()}

        return dct
