import unittest

from src.data_aggregator import DataAggregator, CompanyData


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
        expected = CompanyData(
            stock_price=111,
            long_moving_average_trend=10,
            velocity_of_trend=10,
            long_moving_average_stock_trend=10,
            velocity_of_stock_trend=10,
        )

        aggregator = DataAggregator(**mocked_company_data)
        company_data = aggregator.get_company_data("AMZN", 7, 2010)

        self.assertEqual(company_data, expected)

    def test_calculate_long_moving_average(self):
        cases = [
            [[1, 2, 3, 4, 5, 6, 7], None, 4],
            [range(1001), 100, 950],
            [range(11), 100, 5],
        ]

        for seq, cursor, memory, expected in cases:
            moving_average = DataAggregator.calculate_moving_average(seq, memory)

            self.assertEqual(moving_average, expected)
