from requests import post
from bs4 import BeautifulSoup
from textwrap import fill
from tabulate import tabulate
from configparser import ConfigParser

INI_FILE = 'fox.ini'


def main():
    config = ConfigParser()
    config.read(INI_FILE)

    url = config.get('tracking', 'url')

    data = {
        'action': 'tracking',
        'n': config.get('tracking', 'num')
    }

    response = post(url, data=data)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        header = soup.find_all('tr')[0]
        last_tr = soup.find_all('tr')[-1]

        header_data = [cell.get_text(strip=True) for cell in header.find_all('td')]
        row_data = [cell.get_text(strip=True) for cell in last_tr.find_all('td')]
        row_data_wrapped = [fill(text, width=50) for text in row_data]
        table_data = [row_data_wrapped]
        print(f"\n{tabulate(table_data, headers=header_data, tablefmt='simple')}\n")

    else:
        print(f"Failed to fetch data: ", response.status_code)


if __name__ == '__main__':
    main()
