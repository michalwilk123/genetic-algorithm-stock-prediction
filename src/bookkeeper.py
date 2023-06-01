from .data_aggregator import DataAggregator


class BookKeeperException(Exception):
    ...


class BookKeeper:
    def __init__(self, balance: int, market_data: DataAggregator) -> None:
        self.balance = balance

    def buy_stock(amount: float):
        ...
