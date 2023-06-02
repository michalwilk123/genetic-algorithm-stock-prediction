from logging import getLogger

from .constants import LOG_LEVEL, TRANSACTION_FEE
from .data_aggregator import DataAggregator, Month, Year

logger = getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class BookKeeperException(Exception):
    ...


class BookKeeper:
    """
    This class stores agent transactions and assignes them
    correct price for buying/selling
    """

    def __init__(self, balance: int, market_data: DataAggregator) -> None:
        self.balance = balance
        self._transactions = []

    def buy_stock(self, amount: float, symbol: str, month: Month, year: Year):
        if not self.balance >= amount:
            return

        if 0 < amount < 10:
            return

        if amount < 0:
            self._round_up_selling_amount(symbol, amount)

        self.balance -= amount

    @property
    def number_of_transactions(self):
        ...

    @property
    def invested_companies(self):
        ...

    @property
    def balance(self):
        ...

    def close_position(self, month: Month, year: Year):
        """
        Sells everything
        """
        ...
