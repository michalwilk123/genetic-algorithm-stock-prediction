import unittest

from genetic_algorithm_stock_prediction.bookkeeper import (
    BookKeeper,
    BookKeeperException,
)
from genetic_algorithm_stock_prediction.constants import DataAggregatorProps
from genetic_algorithm_stock_prediction.data_aggregator import DataAggregator, DataAggregatorError
from genetic_algorithm_stock_prediction.constants import TRANSACTION_FEE

data_aggregator = DataAggregator(**DataAggregatorProps)


class TestBookkeeper(unittest.TestCase):
    def test_happy_path(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        bookkeeper.make_transaction(100, "AAPL", 10, 2020)
        bookkeeper.make_transaction(1000, "IBM", 1, 2011)
        bookkeeper.make_transaction(10.5, "IBM", 1, 2011)
        bookkeeper.make_transaction(1000, "VWAGY", 7, 2015)

        bookkeeper.make_transaction(-1000, "VWAGY", 7, 2015)

        self.assertEqual(bookkeeper.number_of_transactions, 5)
        self.assertEqual(bookkeeper.invested_companies, 3)
        self.assertEqual(bookkeeper.balance, 10_000 - 1110.5 - 4 * TRANSACTION_FEE)

    def test_should_not_allow_selling_not_owned_stock(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        bookkeeper.make_transaction(-1000, "IBM", 1, 2011)

        self.assertEqual(bookkeeper.number_of_transactions, 0)

    def test_selling(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)
        bookkeeper.make_transaction(1000, "BMW.DE", 1, 2011)
        bookkeeper.make_transaction(-1000, "BMW.DE", 1, 2011)

        self.assertEqual(bookkeeper.number_of_transactions, 2)
        self.assertEqual(bookkeeper.balance, 10_000 - TRANSACTION_FEE)

    def test_should_sell_all_if_below_threshhold(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        bookkeeper.make_transaction(1000, "BMW.DE", 1, 2011)
        bookkeeper.make_transaction(-10_000, "BMW.DE", 1, 2011)

        self.assertEqual(bookkeeper.number_of_transactions, 2)
        self.assertEqual(bookkeeper.balance, 10_000 - TRANSACTION_FEE)

    def test_should_not_be_able_to_buy_not_available_stock(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        # NSWE was not listed at this date
        bookkeeper.make_transaction(1000, "NWSA", 6, 2010)

        self.assertEqual(bookkeeper.number_of_transactions, 0)
        self.assertEqual(bookkeeper.balance, 10_000)

    def test_should_not_be_able_to_buy_wierd_stock_amounts(self):
        bookkeeper = BookKeeper(10_000, data_aggregator)

        wierd_cases = [0, -10, 4]

        for case in wierd_cases:
            bookkeeper.make_transaction(case, "AMZN", 6, 2015)

        self.assertEqual(bookkeeper.number_of_transactions, 0)
        self.assertEqual(bookkeeper.balance, 10_000)

    def test_should_buy_as_much_as_possible_when_not_enough_money(self):
        bookkeeper = BookKeeper(100, data_aggregator)

        bookkeeper.make_transaction(11, "BAYN.DE", 10, 2020)
        bookkeeper.make_transaction(10_000, "BAYN.DE", 10, 2020)

        # should be able to buy this
        bookkeeper.make_transaction(100, "BAYN.DE", 10, 2020)

        position = bookkeeper.calculate_current_position("BAYN.DE", 10, 2020)

        self.assertEqual(bookkeeper.number_of_transactions, 2)
        self.assertEqual(position, 100 - TRANSACTION_FEE * 2)

    def test_calculate_position(self):
        cases = [
            [[(6, 2010), (8,2010)], [10, 60], -30],
            [[(6, 2010), (8,2010)], [10, 6000], -3000],
            [[(6, 2010), (7,2010), (8,2010)], [10, 1000, -1000], 1500],
        ]
        end_date = (9,2010)
        mocked_aggregator = {
            "stock_prices": {"GOOGL": [100, 50, 200, 100]},
            "opinions": {"GOOGL": []},
            "stock_trends": {"GOOGL": []},
        }
        data_aggregator = DataAggregator(**mocked_aggregator)

        for transaction_dates, transaction_amounts, expected_profit in cases:
            bookkeeper = BookKeeper(10_000, data_aggregator)

            for amount, date in zip(transaction_amounts, transaction_dates):
                bookkeeper.make_transaction(amount, "GOOGL", *date)
            
            bookkeeper.close_position(*end_date)
            position = bookkeeper.balance
            end_profit = position - 10_000 + 2 * TRANSACTION_FEE

            self.assertEqual(end_profit, expected_profit)
