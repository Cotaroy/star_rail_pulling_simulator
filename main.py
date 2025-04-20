"""run star rail pulling similator (mainly for testing)"""

from player_classes import Player
from loading import load_light_cone_banner, load_limited_banner, load_player_data, load_standard_banner
from validate import *


if __name__ == '__main__':

    running = True

    while running:
        print('What would u like to do?')
        print('1: Create a new Save')
        print('2: Load a Save')
        print('3: Quit')

        choices = ['1', '2', '3']
        inp = input()

        inp = validate_choice(inp, choices)

        if inp == '3':
            running = False
            print('Quitting...')
            break

        if inp == '1':
            print('What do you want the id of the new save to be?')
            inp = input('NOTE: identical id to existing save will overwrite old save\n')

            inp = validate_id_overwrite(inp)

            print('Creating new player save...')
            player = Player(inp)
            print(inp)
            player.save()
        else:
            inp = input('Enter the id of the save you would like to load.\n')

            validate_id(inp)
            print('Loading player save...')
            player = load_player_data(inp)

        choosing_banner = True
        while choosing_banner:

            print('What banner do you want to pull on?')
            print('1: standard')
            print('2: limited')
            print('3: light cone')
            print('4: quit choosing banner')
            inp = input()
            inp = validate_choice(inp, {'1', '2', '3', '4'})

            if inp == '4':
                choosing_banner = False
                break

            if inp == '1':
                banner = load_standard_banner(player.pity.standard_pity)
            else:
                print('What version?')
                print('Must be valid version.')
                version = input()
                version = validate_banner(version)

                if inp == '2':
                    banner = load_limited_banner(player.pity.limited_pity)
                else:
                    banner = load_light_cone_banner(player.pity.light_cone_pity)

            pulling = True
            while pulling:
                print('-------------------------------')
                print('What would you like to do?')
                print('1: do a single pull')
                print('2: do a ten pull')
                print('3: show inventory')
                print('4: show pity')
                print('5: save')
                print('6: quit pulling')
                print('-------------------------------')

                choices = ['1', '2', '3', '4', '5', '6']
                inp = input()
                inp = validate_choice(inp, choices)

                print('-------------------------------')
                if inp == '1':
                    player.pull(1, banner)
                elif inp == '2':
                    player.pull(10, banner)
                elif inp == '3':
                    player.show_inventory()
                elif inp == '4':
                    player.show_pity()
                elif inp == '5':
                    player.save()
                    print('Saving...')
                else:
                    pulling = False
                    print('Quitting...')
