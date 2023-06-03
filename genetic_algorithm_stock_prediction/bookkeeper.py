import math
from collections import Counter, defaultdict
from logging import getLogger
from typing import NamedTuple

import numpy as np

from .constants import LOG_LEVEL, TRANSACTION_FEE
from .data_aggregator import DataAggregator, Month, Year

logger = getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class Transaction(NamedTuple):
    symbol: str
    amount: float
    month: Month
    year: Year


class BookKeeperException(Exception):
    ...


class BookKeeper:
    """
    This class stores agent transactions and assignes them
    correct price for buying/selling
    """

    def __init__(self, balance: int, data_aggregator: DataAggregator) -> None:
        self._balance = balance
        self._transactions: list[Transaction] = []
        self._data_aggregator = data_aggregator

    def calculate_transaction_costs(
        self, amount: float, symbol: str, month: Month, year: Year
    ) -> tuple[float, float] | None:
        if not self._data_aggregator.is_stock_price_available(symbol, month, year):
            return None

        if amount > 0:
            transaction_cost = min(self._balance, amount + TRANSACTION_FEE)
            amount = transaction_cost - TRANSACTION_FEE

            if self._balance <= TRANSACTION_FEE or amount < 10:
                return None
        else:
            company_stake = self.calculate_current_position(symbol, month, year)
            """
            If agent want to sell more than it possible, bookkeeper
            will round-up to buy all available balance
            """
            amount = max(-company_stake, amount)
            transaction_cost = amount

            if amount > -10:
                return None

        return amount, transaction_cost

    def make_transaction(self, amount: float, symbol: str, month: Month, year: Year):
        calculated = self.calculate_transaction_costs(amount, symbol, month, year)

        if calculated is None:
            return

        value, cost = calculated

        self._balance -= cost

        assert self._balance >= 0, "Cannot buy more than account balance amount"

        self._transactions.append(Transaction(symbol, value, month, year))

    def calculate_current_position(
        self, company_symbol: str, month: Month, year: Year
    ) -> int:
        position = 0

        for transaction in filter(
            lambda tr: tr.symbol == company_symbol, self._transactions
        ):
            company_data = self._data_aggregator.get_company_data(
                transaction.symbol, transaction.month, transaction.year
            )
            position += transaction.amount / company_data.stock_price

        present_data = self._data_aggregator.get_company_data(
            company_symbol, month, year
        )

        return present_data.stock_price * position

    @property
    def number_of_transactions(self) -> int:
        return len(self._transactions)

    @property
    def average_transaction(self) -> float:
        return np.mean([abs(ts.amount) for ts in self._transactions])

    @property
    def number_of_invested_companies(self) -> int:
        return len(Counter(transaction.symbol for transaction in self._transactions))

    @property
    def companies_by_invested_amount(self):
        companies = defaultdict(lambda: 0)

        for transaction in filter(lambda tr: tr.amount > 0, self._transactions):
            companies[transaction.symbol] += transaction.amount

        return dict(sorted(companies.items(), key=lambda item: -item[1]))

    @property
    def balance(self):
        return self._balance

    def close_position(self, month: Month, year: Year, write: bool = True):
        """
        Sell everything
        """
        symbols = set(transaction.symbol for transaction in self._transactions)

        if not write:
            num_of_all_transactions = self.number_of_transactions
            balance = self._balance

        for symbol in symbols:
            self.make_transaction(-math.inf, symbol, month, year)

        if not write:
            self._transactions = self._transactions[:num_of_all_transactions]
            self._balance = balance
