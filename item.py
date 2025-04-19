
from dataclasses import dataclass


@dataclass
class Item:
    """
    anything that can be pulled

    name: name of the item
    star: how many stars it is
    """
    name: str
    star: int

    def __str__(self):
        stars = ''
        for _ in range(self.star):
            stars += '★'
        return f'{self.name} {stars}'
