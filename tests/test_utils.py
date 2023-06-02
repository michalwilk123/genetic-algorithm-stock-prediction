import unittest
from itertools import zip_longest

from genetic_algorithm_stock_prediction.utils import (
    calculate_next_date,
    create_month_year_generator,
    create_n_pairs_from_elements,
)


class TestUtilities(unittest.TestCase):
    def test_mth_year_generator_simple(self):
        start = (10, 2010)
        end = (4, 2011)
        expected_dates = [
            (10, 2010),
            (11, 2010),
            (12, 2010),
            (1, 2011),
            (2, 2011),
            (3, 2011),
            (4, 2011),
        ]

        for date, expected in zip_longest(
            create_month_year_generator(start, end), expected_dates
        ):
            self.assertEqual(date, expected)

    def test_mth_year_generator_multiple(self):
        cases = [
            [(1, 2010), (1, 2010), 1],
            [(1, 2010), (2, 2010), 2],
            [(1, 2010), (12, 2010), 12],
            [(1, 2010), (1, 2015), 5 * 12 + 1],
        ]

        for start, end, expected_count in cases:
            count = 0

            for _ in create_month_year_generator(start, end):
                count += 1

            self.assertEqual(count, expected_count)

    def test_calculate_next_month(self):
        cases = [
            [(10, 2010), 0, (10, 2010)],
            [(10, 2010), 12, (10, 2011)],
            [(12, 2010), 12, (12, 2011)],
            [(10, 2010), -12, (10, 2009)],
            [(10, 2010), 12 * 100, (10, 2110)],
        ]

        for start_date, delta, expected in cases:
            calculated = calculate_next_date(start_date, delta)

            self.assertEqual(calculated, expected)

    def test_create_n_pairs_from_elements(self):
        elements = [10, 11, 22, 33, 44, 55, 66, 77, 88, 99]
        produced = 100

        pairs = create_n_pairs_from_elements(elements, produced)

        for elem1, elem2 in pairs:
            self.assertTrue(elem1 != elem2)
            self.assertTrue(elem1 in elements)
            self.assertTrue(elem2 in elements)
