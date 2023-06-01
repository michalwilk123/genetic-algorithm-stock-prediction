import csv
import dataclasses
import re
from collections import defaultdict
from collections.abc import Sequence
from functools import lru_cache
from typing import Literal, NamedTuple, get_args

import numpy as np

from .constants import CONSUMER_RECALL, SHORT_CONSUMER_RECALL


@dataclasses.dataclass
class CompanyData:
    stock_price: float
    long_moving_average_trend: float
    velocity_of_trend: float
    long_moving_average_stock_trend: float
    velocity_of_stock_trend: float


Month = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Year = Literal[
    2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023
]


class Scalers(NamedTuple):
    VelocityScaler: int = 10
    LMAScaler: int = 100


class DataAggregator:
    DATE_PATTERN = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})")

    def __init__(
        self,
        stock_prices: str | dict[str, list[float]],
        opinions: str | dict[str, list[float]],
        stock_trends: str | dict[str, list[float]],
        *,
        scalers: Scalers | None = None,
    ) -> None:
        self._scalers = scalers or Scalers()

        if isinstance(stock_prices, str):
            self._stock_price = self.create_dict_from_file(stock_prices, "shortDate")
        else:
            self._stock_price = stock_prices

        if isinstance(opinions, str):
            self._opinions = self.create_dict_from_file(opinions, "Date")
        else:
            self._opinions = opinions

        if isinstance(opinions, str):
            self._stock_opinions = self.create_dict_from_file(stock_trends, "Date")
        else:
            self._stock_opinions = stock_trends

    @lru_cache(maxsize=1024)
    def get_company_data(
        self, company_symbol: str, month: Month, year: Year
    ) -> CompanyData:
        idx = self.calculate_index(month, year)

        stock_price = self._stock_price[company_symbol][idx]
        opinions = self._opinions[company_symbol]
        stock_opinions = self._stock_opinions[company_symbol]

        lma_trend = self.calculate_moving_average_trend(opinions)
        lma_stock_trend = self.calculate_moving_average_trend(stock_opinions)

        vel_trend = self.calculate_velocity(opinions)
        vel_stock_trend = self.calculate_velocity(stock_opinions)

        return CompanyData(
            stock_price=stock_price,
            long_moving_average_trend=lma_trend,
            long_moving_average_stock_trend=lma_stock_trend,
            velocity_of_trend=vel_trend,
            velocity_of_stock_trend=vel_stock_trend,
        )

    @staticmethod
    def create_date_index(month: Month, year: Year) -> str:
        return f"{year}-{month}"

    def calculate_velocity(self, records: Sequence) -> float:
        return np.tanh(
            DataAggregator.calculate_moving_average(
                records, memory=SHORT_CONSUMER_RECALL
            )
            / (
                DataAggregator.calculate_moving_average(records, memory=CONSUMER_RECALL)
                * self._scalers.VelocityScaler
            )
        )

    def calculate_moving_average_trend(self, records: Sequence) -> float:
        return (
            DataAggregator.calculate_moving_average(records) / self._scalers.LMAScaler
        )

    @staticmethod
    def text_string_to_index(string: str) -> int:
        parsed = re.search(DataAggregator.DATE_PATTERN, string)

        assert (
            parsed is not None
        ), f"Value should match the pattern: {DataAggregator.DATE_PATTERN}"
        year, month = map(int, parsed.groups(("year", "month")))

        assert year in get_args(Year), "Year should be in range: 2010 - 2023"
        assert month in get_args(Month), "Month should be in range 1 - 12"

        return DataAggregator.calculate_index(month, year)

    @staticmethod
    def calculate_index(month: Month, year: Year) -> int:
        return get_args(Year).index(year) * 12 + get_args(Month).index(month) - 5

    @staticmethod
    def create_dict_from_file(
        path: str, index_column_name: str
    ) -> dict[str, list[float]]:
        data_dict = defaultdict(lambda: [])

        with open(path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    if key == index_column_name:
                        continue

                    try:
                        data_dict[key].append(float(value))
                    except ValueError:
                        data_dict[key].append(float("nan"))

        return data_dict

    @staticmethod
    def calculate_moving_average(
        records: Sequence, cursor: int, *, memory: int | None = None
    ):
        memory = memory or CONSUMER_RECALL
        return np.mean(records[max(cursor - memory, 0) : cursor])
