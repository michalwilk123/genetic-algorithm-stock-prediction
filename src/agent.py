from typing import NamedTuple

import numpy as np

from bookkeeper import BookKeeper
from stocks import Sectors, stocks_symbols

from .constants import FIELDS_TO_MUTATE, LOG_LEVEL, MUTATION, NUMBER_OF_SECTORS
from .data_aggregator import CompanyData, DataAggregator, Month, Year


class AgentInputs(NamedTuple):
    courage: float
    amount_multiplier: float

    stock_trend_bias: float
    trend_bias: float

    stock_trend_velocity_bias: float
    trend_velocity_bias: float

    sector_biases: dict[Sectors, float]
    company_biases: dict[str, float]

    @classmethod
    def from_flat(cls, array: list[float]) -> "AgentInputs":
        sector_biases = {
            sector.name: value
            for sector, value in zip(Sectors, array[6 : 6 + NUMBER_OF_SECTORS])
        }
        company_biases = {
            stock.name: value
            for stock, value in zip(stocks_symbols, array[6 + NUMBER_OF_SECTORS])
        }

        return cls(
            courage=array[0],
            amount_multiplier=array[1],
            stock_trend_bias=array[2],
            trend_bias=array[3],
            stock_trend_velocity_bias=array[4],
            trend_velocity_bias=array[5],
            sector_biases=sector_biases,
            company_biases=company_biases,
        )

    def to_flat(self) -> list[float]:
        return [
            self.courage,
            self.amount_multiplier,
            self.stock_trend_bias,
            self.trend_bias,
            self.stock_trend_velocity_bias,
            self.trend_velocity_bias,
            *self.sector_biases.values(),
            *self.company_biases,
        ]

    @classmethod
    def init_random(cls) -> "AgentInputs":
        return cls(*np.random.random_sample(8))

    @classmethod
    def from_parents(
        cls, father_chromosomes: "AgentInputs", mother_chromosomes: "AgentInputs"
    ) -> "AgentInputs":
        n_of_fields = len(father_arr)

        father_arr = np.array(father_chromosomes)
        mother_arr = np.array(mother_chromosomes)

        child = (father_arr + mother_arr) / 2

        noise = np.random.random_sample(FIELDS_TO_MUTATE) * 2 - 1
        noise *= MUTATION

        fields_to_change = np.choice(n_of_fields, FIELDS_TO_MUTATE, replace=False)

        mutation = child(n_of_fields)
        mutation[fields_to_change] = noise

        child = (child + mutation) / 2

        return cls(*child)


class Agent:
    def __init__(
        self,
        start_balance: int,
        min_transaction: int,
        max_transaction: int,
        data_aggregator: DataAggregator,
        inputs: AgentInputs,
    ) -> None:
        self._start_balance = start_balance
        self._min_transaction = min_transaction
        self._max_transaction = max_transaction
        self._data_aggregator = data_aggregator
        self._inputs = inputs

        self._bookkeeper = BookKeeper(self._start_balance, data_aggregator)

    @property
    def inputs(self):
        return self._inputs

    def create_genes(self):
        ...

    def fitness(self):
        ...

    def run_month(self, month: Month, year: Year) -> None:
        ...

    def _calculate_decision(self, company_data: CompanyData) -> float:
        weights = np.array(
            [
                company_data.long_moving_average_stock_trend
                * self._inputs.stock_trend_bias,
                company_data.long_moving_average_trend * self._inputs.trend_bias,
                company_data.name * self._inputs.trend_bias,
            ]
        )

        decision = np.tanh(np.sum(weights))
        return decision

    def show_stats(self):
        ...


class AgentBuilder:
    def __init__(
        self,
        start_balance: int,
        min_transaction: int,
        max_transaction: int,
        data_aggregator: DataAggregator,
    ) -> None:
        self._start_balance = start_balance
        self._min_transaction = min_transaction
        self._max_transaction = max_transaction
        self._data_aggregator = data_aggregator

    @staticmethod
    def from_parents(parent1: Agent, parent2: Agent) -> Agent:
        child_genes = AgentInputs.from_parents(parent1, parent2)
        return Agent(child_genes)

    @staticmethod
    def initialize_random() -> Agent:
        agent_genes = AgentInputs.init_random()
        return Agent(agent_genes)
