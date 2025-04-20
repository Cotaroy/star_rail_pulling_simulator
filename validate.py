"""validating functions"""
from loading import find_file
from loading import load_rate_up

from constants import PLAYER_DATA_FOLDER_FILE_PATH, PLAYER_DATA_NAME_TEMPLATE
from constants import RATE_UP_FILE_PATH


def validate_choice(inp: str, choices: list | set) -> str:
    """run until inp in choices"""
    while inp not in choices:
        inp = input('Please select a valid choice.\n')
    return inp


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


def validate_banner(inp: str) -> str:
    """
    validate that inp is a valid banner

    inp is valid if
    - inp in rate_up.json
    """
    rate_up = load_rate_up(RATE_UP_FILE_PATH)
    while inp not in rate_up:
        inp = input('Please enter a valid choice. \n')
    return inp

