import itertools
import random
from typing import Generator, get_args

from .data_aggregator import Month, Year


def create_month_year_generator(
    start: tuple[Month, Year], end: tuple[Month, Year]
) -> Generator[tuple[Month, Year], None, None]:
    assert (
        start[0] + start[1] * 12 <= end[0] + end[1] * 12
    ), "Start date should be earlier than end date!"

    start_month, start_year = start

    month_iterator = itertools.islice(
        itertools.cycle(get_args(Month)), start_month - 1, None
    )

    year_iterator = itertools.count(start_year)

    for year in year_iterator:
        for month in month_iterator:
            yield month, year

            if (month, year) == end:
                return

            if month == 12:
                break


def calculate_next_date(date: tuple[Month, Year], delta: int):
    month, year = date

    next_year, next_month = divmod(year * 12 + month + delta, 12)

    if next_month == 0:
        next_year -= 1
        next_month = 12

    return next_month, next_year


def create_n_pairs_from_elements(elements: list, n: int) -> list[int]:
    return [random.sample(elements, k=2) for _ in range(n)]
