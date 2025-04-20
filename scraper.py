"""scrape website to get rate up details"""
import json

from bs4 import BeautifulSoup
import requests

from constants import WEB_ADDRESS, SCRAPE_TARGET_HTML_NAME, RATE_UP_FILE_PATH


def refresh():
    """refresh the to_be_scraped.html"""
    _get_html(WEB_ADDRESS, SCRAPE_TARGET_HTML_NAME)
    _prettify(SCRAPE_TARGET_HTML_NAME)


def _get_html(web_address, name):
    """
    get the html file to be scraped and save it as to_be_scraped.html
    """
    r = requests.get(web_address)

    with open(name, 'w', encoding='utf-8') as f:
        f.write(r.text)


def _prettify(file_path):
    """prettify"""
    with open(file_path, 'r') as f:
        doc = BeautifulSoup(f, 'html.parser')
    pretty = doc.prettify()
    f.close()
    with open(file_path, 'w') as f:
        f.write(pretty)
    f.close()


def build_dictionary(file_path) -> dict:
    """build rate up dictionary"""
    with open(file_path, 'r') as f:
        doc = BeautifulSoup(f, 'html.parser')

    dict = {}

    lines = doc.find_all('th')
    for i in range(len(lines)):
        version = lines[i].text
        if 'Phase' in lines[i].text:
            version = version.replace('Phase', '.')
            for word in {'Warp', 'Banners', 'Version', ' '}:
                version = version.replace(word, '')
            version = version.strip()
            dict[version] = {"limited": {"5": [], "4": []}, "light cone": {"5": [], "4": []}}

            alt_texts = lines[i].find_next('div').find_all('img')

            for j in range(len(alt_texts)):
                alt_text = alt_texts[j].get('alt')
                alt_text = alt_text.replace('HSR - ', '')
                dict[version]['limited']['5'].append(alt_text)

            current = alt_texts[-1]

            searching = True
            while searching:
                current = current.next_element
                if current == lines[i + 1]:
                    searching = False
                if current.name == 'div':
                    alt_texts = current.find_all('img')

                    for j in range(len(alt_texts)):
                        current = alt_texts[j]
                        alt_text = alt_texts[j].get('alt')
                        alt_text = alt_text.replace('HSR - ', '')
                        dict[version]['limited']['4'].append(alt_text)

                    alt_texts = current.find_next('div').find_all('img')

                    for j in range(len(alt_texts)):
                        current = alt_texts[j]
                        alt_text = alt_texts[j].get('alt')
                        alt_text = alt_text.replace('HSR - ', '')
                        dict[version]['light cone']['5'].append(alt_text)

                    alt_texts = current.find_next('div').find_all('img')

                    for j in range(len(alt_texts)):
                        alt_text = alt_texts[j].get('alt')
                        alt_text = alt_text.replace('HSR - ', '')
                        dict[version]['light cone']['4'].append(alt_text)

                    searching = False
    return dict


def save_dictionary(file_path: str, dct: dict):
    """save dictionary to file_path"""
    with open(file_path, 'w') as file:
        json.dump(dct, file, **{'indent': 4})


if __name__ == '__main__':
    refresh()
    dct = build_dictionary(SCRAPE_TARGET_HTML_NAME)
    save_dictionary(RATE_UP_FILE_PATH, dct)
