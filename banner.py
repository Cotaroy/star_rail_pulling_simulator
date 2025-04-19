"""banner classes"""

from __future__ import annotations
from item import Item
from pity import Pity
from dataclasses import dataclass

import random

from pity import LimitedPity


@dataclass
class Banner:
    """
    a banner you can pull on

    Instance Attributes:
    - loot_pool: dictionary of items that can be pulled {star: Item}
    - pity: the pity on this banner
    """
    loot_pool: dict[int: list[Item]]
    pity: Pity

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
            item = self.pull_four_star()
            self.pity.change_pity(item)
            return item
        # pulled a three star
        else:
            item = random.choice(self.loot_pool[3])
            self.pity.change_pity(item)
            return item

    def pull_five_star(self) -> Item:
        """return a random five star"""
        return random.choice(self.loot_pool[5])

    def pull_four_star(self) -> Item:
        """return a random four star"""
        return random.choice(self.loot_pool[4])


class LimitedBanner(Banner):
    """
    a limited banner you can pull on

    Instance Attributes:
    - loot_pool: dictionary of items that can be pulled {star: Item}
    - five_star_rate_up: the five star item that is on rate_up
    - four_star_rate_up: the four star items that are on rate_up
    """
    five_star_rate_up: Item
    four_star_rate_up: list[Item]
    pity: LimitedPity

    def __init__(self, loot_pool, five, four, pity):
        super().__init__(loot_pool, pity)
        self.five_star_rate_up = five
        self.four_star_rate_up = four

    def pull_five_star(self) -> Item:
        """return a random five star based on gaurantee and rate up"""
        if self.pity.gaurantee:
            self.pity.gaurantee = False
            return self.five_star_rate_up
        else:
            rand = random.randint(1, 2)
            if rand == 1:
                return self.five_star_rate_up
            self.pity.gaurantee = True
            return random.choice(self.loot_pool[5])

    def pull_four_star(self) -> Item:
        """return a random four star based on rate up"""
        rand = random.randint(1, 2)
        if rand == 1:
            return random.choice(self.four_star_rate_up)
        return random.choice(self.loot_pool[4])

