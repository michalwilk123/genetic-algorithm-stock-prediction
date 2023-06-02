import unittest

from genetic_algorithm_stock_prediction.bookkeeper import (
    BookKeeper,
    BookKeeperException,
)
from genetic_algorithm_stock_prediction.constants import DataAggregatorProps
from genetic_algorithm_stock_prediction.data_aggregator import DataAggregator

data_aggregator = DataAggregator(**DataAggregatorProps)


class TestBookkeeper(unittest.TestCase):
    def test_happy_path(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        bookkeeper.buy_stock(100, "AAPL", 10, 2020)
        bookkeeper.buy_stock(1000, "IBM", 1, 2011)
        bookkeeper.buy_stock(10.5, "IBM", 1, 2011)
        bookkeeper.buy_stock(1000, "VWAGY", 7, 2015)

        bookkeeper.buy_stock(-1000, "VWAGY", 7, 2015)

        self.assertEqual(bookkeeper.number_of_transactions, 4)
        self.assertEqual(bookkeeper.invested_companies, 3)
        self.assertEqual(bookkeeper.balance, 3)

    def test_should_not_allow_selling_not_existing(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        bookkeeper.buy_stock(-1000, "IBM", 1, 2011)

        self.assertEqual(bookkeeper.number_of_transactions, 0)

    def test_should_sell_all_if_below_threshhold(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        bookkeeper.buy_stock(1000, "IBM", 1, 2011)
        bookkeeper.buy_stock(-10_000, "IBM", 1, 2011)

        self.assertEqual(bookkeeper.number_of_transactions, 2)
        self.assertEqual(bookkeeper.balance, 10_000)
