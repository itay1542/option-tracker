from data_sources.symbols.symbols_datasource import SymbolsDataSource
from data_sources.symbols.wikipedia import wikipedia_page_to_symbol_list


class SNP500Symbols(SymbolsDataSource):
    def get_symbols(self):
        return wikipedia_page_to_symbol_list('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 0)