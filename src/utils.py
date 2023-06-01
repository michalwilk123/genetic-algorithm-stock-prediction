import itertools
from typing import Generator, get_args

from .data_aggregator import Month, Year


def create_month_year_generator(
    start: tuple[Month, Year], end: tuple[Month, Year]
) -> Generator[tuple[Month, Year], None, None]:
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
    return next_month, next_year
