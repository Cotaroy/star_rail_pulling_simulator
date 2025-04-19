"""run star rail pulling similator (mainly for testing)"""

from player_classes import Player
from loading import load_items
from banner import Banner

FILE_PATH = 'standard_banner.json'

if __name__ == '__main__':
    player = Player()

    standard_pool = load_items(FILE_PATH)

    standard_banner = Banner(standard_pool, player.pity.standard_pity)
