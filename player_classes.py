"""player classes"""

from __future__ import annotations

from item import Item
from pity import StandardPity, LightConePity, LimitedPity
from banner import Banner


class Player:
    """
    player class

    Instance Attributes
    - inventory: dictionary {item_name: number of that item}
    - pity: how many pulls since last five star
    """
    inventory: Inventory
    pity: PlayerPity

    def __init__(self):
        self.inventory = Inventory()
        self.pity = PlayerPity()

    def show_inventory(self):
        """show inventory"""
        print(self.inventory)

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
            self.inventory.add_to_inventory(item)
            print(f'You got {str(item)}')


class Inventory:
    """
    inventory of items

    items: [star: dict[Item, number of that Item]]
    """
    items: dict[int, [dict[Item, int], dict[Item, int], dict[Item, int]]] | dict[int: dict]

    def __init__(self, items=None):
        if items is None:
            items = {5: {}, 4: {}, 3: {}}
        self.items = items

    def __str__(self):
        five_stars = ''
        for item in self.items[5]:
            five_stars += f'|||{item} : {self.items[5][item]}\n'

        four_stars = ''
        for item in self.items[4]:
            four_stars += f'|||{item} : {self.items[4][item]}\n'

        three_stars = ''
        for item in self.items[3]:
            three_stars += f'|||{item} : {self.items[3][item]}\n'

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
        if item not in self.items[star]:
            self.items[star][item] = 1
        else:
            self.items[star][item] += 1


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
                 f'Limited Pity: {str(self.limited_pity)}\n'
                 f'Light Cone Pity: {str(self.light_cone_pity)}\n'
                 f'Standard Pity: {str(self.standard_pity)}\n'
                 f'---------------------\n')
        return build

