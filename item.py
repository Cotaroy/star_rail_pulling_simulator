
from dataclasses import dataclass


@dataclass
class Item:
    """
    anything that can be pulled

    name: name of the item
    star: how many stars it is
    type: type of item

    type in {'character', 'light cone'}

    """
    name: str
    star: int
    type: str

    def __str__(self):
        if self.star == 3:
            return self.name
        stars = ''
        for _ in range(self.star):
            stars += '★'
        if self.star == 4:
            return f'{self.name} {stars}'
        if self.star == 5:
            return f'{stars} {self.name} {stars}'

