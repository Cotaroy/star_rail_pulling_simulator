"""run star rail pulling similator (mainly for testing)"""

from player_classes import Player
from loading import load_limited_banner, load_player_data, find_file, load_standard_banner


PLAYER_DATA_FOLDER_FILE_PATH = 'json/player_data/'

# file_name would be f'{PLAYER_DATA_NAME_TEMPLATE}_{id}.json'
PLAYER_DATA_NAME_TEMPLATE = 'player_id_'
PLAYER_DATA_NAME_TEMPLATE_WITH_FOLDER = 'json/player_data/player_id_'


def validate_choice(inp: str, choices: list | set) -> None:
    """run until inp in choices"""
    while inp not in choices:
        inp = input('Please select a valid choice.\n')


def validate_id_overwrite(inp: str) -> str:
    """ask for confirmation of overwriting save"""
    file_path = f'{PLAYER_DATA_NAME_TEMPLATE}{inp}.json'
    if find_file(file_path, PLAYER_DATA_FOLDER_FILE_PATH) is not None:
        print(f'This will over write {PLAYER_DATA_FOLDER_FILE_PATH}{PLAYER_DATA_NAME_TEMPLATE}{inp} \n'
              f'are you sure?')
        confirm = input('Y/N\n').upper()
        validate_choice(confirm, ['Y', 'N'])

        if confirm == 'Y':
            print('Ok, overwriting save.')
            return inp
        else:
            inp = input('Please pick a new id.\n')
            return validate_id_overwrite(inp)

    else:
        print('This is a new id.')
        return inp


def validate_id(inp: str):
    """validate that inp is an id of a save"""
    file_path = f'{PLAYER_DATA_NAME_TEMPLATE}{inp}.json'
    if find_file(file_path, PLAYER_DATA_FOLDER_FILE_PATH) is not None:
        return
    else:
        inp = input('Please enter a valid id.\n')
        validate_id(inp)


if __name__ == '__main__':

    running = True

    while running:
        print('What would u like to do?')
        print('1: Create a new Save')
        print('2: Load a Save')
        print('3: Quit')

        choices = ['1', '2', '3']
        inp = input()

        validate_choice(inp, choices)

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

        while running:

            # banner = load_standard_banner(player.pity.standard_pity)
            banner = load_limited_banner(player.pity.limited_pity)

            print('-------------------------------')
            print('What would you like to do?')
            print('1: do a single pull')
            print('2: do a ten pull')
            print('3: show inventory')
            print('4: show pity')
            print('5: save')
            print('6: quit')
            print('-------------------------------')

            choices = ['1', '2', '3', '4', '5', '6']
            inp = input()
            validate_choice(inp, choices)

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
                running = False
                print('Quitting...')
