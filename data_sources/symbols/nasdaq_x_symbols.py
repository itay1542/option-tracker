from typing import List

from data_sources.symbols.symbols_datasource import SymbolsDataSource
from data_sources.symbols.wikipedia import wikipedia_page_to_symbol_list


class NasdaqXSymbols(SymbolsDataSource):
    def get_symbols(self) -> List[str]:
        return wikipedia_page_to_symbol_list('https://en.wikipedia.org/wiki/NASDAQ-100', 1)
