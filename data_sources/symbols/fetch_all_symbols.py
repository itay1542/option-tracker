from data_sources.symbols.etf_symbols import ETFSymbols
from data_sources.symbols.nasdaq_x_symbols import NasdaqXSymbols
from data_sources.symbols.snp500_symbols import SNP500Symbols


def fetch_all_symbols():
    symbol_fetchers = [
        NasdaqXSymbols(),
        SNP500Symbols(),
        ETFSymbols(),
    ]
    symbols = []
    for symbol_fetcher in symbol_fetchers:
        symbols.extend(symbol_fetcher.get_symbols())
    return symbols
