from typing import List

from database.models import Equity, OptionExpirations, OptionData


class OptionChainSnapshot:
    def __init__(self, equity: Equity, expiration: OptionExpirations):
        self.equity = equity
        self.expiration = expiration
        self.options: List[OptionData] = []

    def _add_option(self, option: OptionData):
        option.equity_id = self.equity.id
        option.expiration_id = self.expiration.datetime
        self.options.append(option)

    async def create_from_stream(self, stream):
        pass

