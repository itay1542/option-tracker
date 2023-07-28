from typing import List

import requests
from bs4 import BeautifulSoup


def wikipedia_page_to_symbol_list(url: str, td_index: int = 0) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})
    symbols = []

    for row in table.findAll('tr')[1:]:
        symbol = row.findAll('td')[td_index].text.strip()
        symbols.append(symbol)

    return symbols
