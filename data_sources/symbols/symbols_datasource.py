import abc


class SymbolsDataSource(abc.ABC):
    @abc.abstractmethod
    def get_symbols(self):
        pass
