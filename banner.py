"""banner classes"""

from __future__ import annotations
from item import Item
from pity import Pity

import random

from star_rail_pulling_simulator.pity import LimitedPity


class Banner:
    """
    a banner you can pull on

    Instance Attributes:
    - loot_pool: dictionary of items that can be pulled {star: Item}
    - pity: the pity on this banner
    """
    loot_pool: dict[int: set[Item]]
    pity: Pity

    def __init__(self, loot_pool, pity=None):
        if pity is None:
            pity = Pity()

        self.loot_pool = loot_pool
        self.pity = pity

    def pull(self) -> Item:
        """
        a single pull on banner

        return Item based on pull chance
        mutates pity by changing incrementing pity
        """
        limit_five = self.pity.get_chance(5) * 1000
        limt_four = self.pity.get_chance(4) * 1000

        num = random.randint(1, 1000)

        # pulled a five star
        if num <= limit_five:
            item = self.pull_five_star()
            self.pity.change_pity(item)
            return item
        # pulled a four star
        elif num <= limt_four + limit_five:
            item = random.choice(self.loot_pool[4])
            self.pity.change_pity(item)
            return item
        # pulled a three star
        else:
            return random.choice(self.loot_pool[3])

    def pull_five_star(self) -> Item:
        """return a random five star"""
        return random.choice(self.loot_pool[5])


class LimitedBanner(Banner):
    """
    a limited banner you can pull on

    Instance Attributes:
    - loot_pool: dictionary of items that can be pulled {star: Item}
    - rate_up: the item that is on rate_up
    """
    rate_up: Item
    pity: LimitedPity

    def __init__(self, rate_up, pity=None):
        if pity is None:
            pity = LimitedPity()

        super().__init__()
        self.rate_up = rate_up
        self.pity = pity

    def pull_five_star(self) -> Item:
        """return a random five star based on gaurantee"""
        if self.pity.gaurantee:
            return self.rate_up
        else:
            return random.choice(self.loot_pool[5])

