import itertools
import math
import unittest

from genetic_algorithm_stock_prediction.constants import (
    CONSUMER_RECALL,
    SHORT_CONSUMER_RECALL,
    DataAggregatorProps,
)
from genetic_algorithm_stock_prediction.data_aggregator import (
    CompanyData,
    DataAggregator,
)


class TestAggregator(unittest.TestCase):
    def test_string_parsing(self):
        cases = {"2010-06": 0, "2017-02": 80, "2023-05": 155}

        for case, expected in cases.items():
            idx = DataAggregator.text_string_to_index(case)

            self.assertEqual(idx, expected)

    def test_string_parsing_should_fail(self):
        cases = [
            "05-2023",
            "2023-14",
            "2000-11",
        ]

        for case in cases:
            with self.assertRaises(AssertionError):
                DataAggregator.text_string_to_index(case)

    def test_get_company_data(self):
        mocked_company_data = {
            "stock_prices": {"AMZN": [100, 111, 112, 113, 114]},
            "opinions": {"AMZN": [10, 10, 12, 13, 15]},
            "stock_trends": {"AMZN": [3, 3, 10, 40, 30]},
        }
        aggregator = DataAggregator(**mocked_company_data)
        company_data = aggregator.get_company_data("AMZN", 7, 2010)

        self.assertTrue(isinstance(company_data, CompanyData))

    def test_happy_path(self):
        cases = [
            [("AMZN", 10, 2020), 160.39],
            [("AAPL", 1, 2012), 12.43],
            [("PFE", 8, 2021), 40.75],
            [("NWSA", 4, 2013), float("nan")],
        ]
        da = DataAggregator(**DataAggregatorProps)

        for case, expected in cases:
            data = da.get_company_data(*case)

            if math.isnan(expected):
                self.assertTrue(math.isnan(data.stock_price))
            else:
                self.assertAlmostEqual(data.stock_price, expected, 1)

    def test_calculate_long_moving_average(self):
        cases = [
            [[1, 2, 3, 4, 5, 6, 7], 6, None, 4],
            [range(1001), 1000, 101, 950],
            [range(1000), 900, 101, 850],
            [range(11), 10, 100, 5],
            [[1, 1, 1, 100, 100, 100, 100, 1, 1, 1], 6, 4, 100],
        ]

        for seq, cursor, memory, expected in cases:
            moving_average = DataAggregator.calculate_moving_average(
                seq, cursor, memory=memory
            )

            self.assertEqual(moving_average, expected)

    def test_calculate_velocity(self):
        huge_movement = [
            *itertools.repeat(1, CONSUMER_RECALL),
            *itertools.repeat(10_000, SHORT_CONSUMER_RECALL),
        ]
        big_movement = [
            *itertools.repeat(1, CONSUMER_RECALL),
            *itertools.repeat(10, SHORT_CONSUMER_RECALL),
        ]
        small_movement = [
            *itertools.repeat(100, CONSUMER_RECALL),
            *itertools.repeat(120, SHORT_CONSUMER_RECALL),
        ]
        negative_movement = [
            *itertools.repeat(100, CONSUMER_RECALL),
            *itertools.repeat(10, SHORT_CONSUMER_RECALL),
        ]

        huge = DataAggregator.calculate_velocity(huge_movement, len(huge_movement) - 1)
        big = DataAggregator.calculate_velocity(big_movement, len(big_movement) - 1)
        small = DataAggregator.calculate_velocity(
            small_movement, len(small_movement) - 1
        )
        negative = DataAggregator.calculate_velocity(
            negative_movement, len(negative_movement) - 1
        )

        self.assertTrue(huge > big > small > negative)

        self.assertTrue(all(map(lambda x: -1 < x < 1, [huge, big, small, negative])))
