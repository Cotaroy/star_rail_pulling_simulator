"""pity classes"""

from __future__ import annotations

from item import Item


class Pity:
    """
    tracks four/five star pity

    Instance Attributes:
    - four_star_pity: four star pity
    - five_star_pity: five star pity
    """
    four_star_pity: int
    five_star_pity: int

    def __init__(self, four=0, five=0):
        self.four_star_pity, self.five_star_pity = four, five

    def __str__(self):
        return f'5: {self.five_star_pity}, \t 4: {self.four_star_pity}'

    def change_pity(self, item: Item):
        """
        mutate pity based on item (what item got pulled)
        """
        if item.star == 4:
            self.four_star_pity = 0
            self.five_star_pity += 1
        elif item.star == 5:
            self.five_star_pity = 0
            self.four_star_pity += 1
        else:
            self.four_star_pity += 1
            self.five_star_pity += 1

    def at_hard_pity(self, star: int):
        """
        return if hard pity is about to be hit

        Precondition: star in [4, 5]
        """
        if star == 4:
            return self.four_star_pity >= 9
        else:
            return self.five_star_pity >= 89

    def get_chance(self, star: int) -> float:
        """
        return the chance of getting an item of star rarity

        TODO get actual chances (constant chances for now)
        """
        if star == 4:
            if self.at_hard_pity(4):
                return 0.994
            return 0.051
        elif star == 5:
            if self.at_hard_pity(5):
                return 1
            return 0.006
        else:
            return 0.943

    def to_list(self):
        """
        to list
        returns [four pity, five pity]
        """
        return [self.four_star_pity, self.five_star_pity]


class LimitedPity(Pity):
    """
    tracks pity for limited banner

    Instance Attributes:
    - same as Pity
    - rate_up: Item that has rate up on this banner
    - gaurantee: if 50/50 is gauranteed win
        self.gaurantee == True -> next 5 star is limited
    """
    rate_up: Item
    gaurantee: bool

    def __init__(self, four=0, five=0, gaur=False):
        super().__init__(four, five)
        self.gaurantee = gaur

    def __str__(self):
        return f'5: {self.five_star_pity}, \t 4: {self.four_star_pity}, \t gaurantee: {self.gaurantee}'

    def change_pity(self, item: Item):
        """
        mutate pity based on item (what item got pulled)
        also changes gaurantee
        """
        if item.star == 4:
            self.four_star_pity = 0
            self.five_star_pity += 1
        elif item.star == 5:
            self.five_star_pity = 0
            self.four_star_pity += 1
            if item != self.rate_up:
                self.gaurantee = True
            else:
                self.gaurantee = False
        else:
            self.four_star_pity += 1
            self.five_star_pity += 1

    def to_list(self):
        """
        to list
        returns [four pity, five pity, gaurantee]
        """
        return [self.four_star_pity, self.five_star_pity, self.gaurantee]


class StandardPity(Pity):
    """identical to Pity"""


class LightConePity(LimitedPity):
    """
    tracks pity for ligth cone banner

    Instance Attributes:
    - same as LimitedPity
    """
    def __init__(self, four=0, five=0, gaur=False):
        super().__init__(four, five, gaur)

    def at_hard_pity(self, star: int):
        """
        return if hard pity is about to be hit

        Precondition: star in [4, 5]
        """
        if star == 4:
            return self.four_star_pity == 9
        else:
            return self.five_star_pity == 80



