from logging import getLogger

from .constants import LOG_LEVEL
from .data_aggregator import DataAggregator

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

    def buy_stock(amount: float):
        ...
