from data_sources.symbols.symbols_datasource import SymbolsDataSource


class ETFSymbols(SymbolsDataSource):
    def get_symbols(self):
        most_optionable_etfs = [
            "SPY",  # SPDR S&P 500 ETF
            "QQQ",  # Invesco QQQ ETF
            "IWM",  # iShares Russell 2000 ETF
            "GLD",  # SPDR Gold Trust
            "GDX",  # VanEck Vectors Gold Miners ETF
            "EEM",  # iShares MSCI Emerging Markets ETF
            "XLF",  # Financial Select Sector SPDR Fund
            "EFA",  # iShares MSCI EAFE ETF
            "XLE",  # Energy Select Sector SPDR Fund
            "VXX",  # iPath S&P 500 VIX Short-Term Futures ETN
            "XLK",  # Technology Select Sector SPDR Fund
            "XLY",  # Consumer Discretionary Select Sector SPDR Fund
            "XLU",  # Utilities Select Sector SPDR Fund
            "XLI",  # Industrial Select Sector SPDR Fund
            "XLV"  # Health Care Select Sector SPDR Fund
        ]
        return most_optionable_etfs