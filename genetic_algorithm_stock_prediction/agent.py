import dataclasses
from typing import NamedTuple

import numpy as np

from .bookkeeper import BookKeeper
from .constants import (
    DIVERSIFICATION_BONUS,
    FIELDS_TO_MUTATE,
    MUTATION,
    MUTATION_FACTOR,
)
from .data_aggregator import CompanyData, DataAggregator, Month, Year
from .stocks import NUMBER_OF_SECTORS, NUMBER_OF_STOCKS, Sectors, stocks_symbols, get_randomized_stock_list
from .utils import create_n_pairs_from_elements

@dataclasses.dataclass
class AgentReport:
    ...

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
            stock_name: value
            for stock_name, value in zip(stocks_symbols, array[6 + NUMBER_OF_SECTORS :])
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
        return np.array(
            [
                self.courage,
                self.amount_multiplier,
                self.stock_trend_bias,
                self.trend_bias,
                self.stock_trend_velocity_bias,
                self.trend_velocity_bias,
                *self.sector_biases.values(),
                *self.company_biases.values(),
            ]
        )

    @classmethod
    def init_random(cls) -> "AgentInputs":
        return cls.from_flat(
            np.random.random_sample(6 + NUMBER_OF_SECTORS + NUMBER_OF_STOCKS)
        )

    @classmethod
    def from_parents(
        cls, father_chromosomes: "AgentInputs", mother_chromosomes: "AgentInputs"
    ) -> "AgentInputs":
        father_arr = np.array(father_chromosomes.to_flat())
        mother_arr = np.array(mother_chromosomes.to_flat())

        n_of_fields = len(father_arr)

        child = (father_arr + mother_arr) / 2

        noise = np.random.random_sample(FIELDS_TO_MUTATE) * 2 - 1
        noise *= MUTATION

        fields_to_change = np.random.choice(
            n_of_fields, FIELDS_TO_MUTATE, replace=False
        )

        mutation = child.copy()
        mutation[fields_to_change] = noise

        child = child * (1 - MUTATION_FACTOR) + mutation * MUTATION_FACTOR

        return cls.from_flat(child)


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

    def run_month(self, month: Month, year: Year) -> None:
        companies = get_randomized_stock_list()

        for symbol in companies:
            company_data = self._data_aggregator.get_company_data(symbol, month, year)
            decision = self._calculate_decision(company_data)

            if abs(decision) > self._inputs.courage:
                amount = decision * self._inputs.amount_multiplier * self._start_balance

                self._bookkeeper.make_transaction(amount, symbol, month, year)
                
    @staticmethod
    def _normalize_bias(bias:float) -> float:
        return bias * 2 - 1

    def _calculate_decision(self, company_data: CompanyData) -> float:

        weights = np.array(
            [
                company_data.long_moving_average_trend * self._normalize_bias(self._inputs.trend_bias),
                company_data.long_moving_average_stock_trend
                * self._normalize_bias(self._inputs.stock_trend_bias),
                company_data.velocity_of_trend * self._normalize_bias(self._inputs.trend_velocity_bias),
                company_data.velocity_of_stock_trend * self._normalize_bias(self._inputs.stock_trend_velocity_bias),
            ]
        )

        decision = np.tanh(np.sum(weights))
        decision += self._normalize_bias(self._inputs.company_biases[company_data.name])
        decision += self._normalize_bias(self._inputs.sector_biases[company_data.sector.name])

        decision /= 3

        return decision

    def get_report(self) -> AgentReport:
        raise NotImplementedError

    def close_positions(self, month:Month, year:Year) -> None:
        self._bookkeeper.close_position(month, year)

    def evaluate(self) -> float:
        end_balance = self._bookkeeper.balance
        diversification_bonus = (
            self._bookkeeper.invested_companies * DIVERSIFICATION_BONUS
        )

        return end_balance + diversification_bonus


class AgentBuilder:
    def __init__(
        self,
        *,
        start_balance: int,
        min_transaction: int,
        max_transaction: int,
        data_aggregator: DataAggregator,
    ) -> None:
        self._start_balance = start_balance
        self._min_transaction = min_transaction
        self._max_transaction = max_transaction
        self._data_aggregator = data_aggregator

    def build(self, inputs: AgentInputs) -> Agent:
        return Agent(
            start_balance=self._start_balance,
            min_transaction=self._min_transaction,
            max_transaction=self._max_transaction,
            data_aggregator=self._data_aggregator,
            inputs=inputs,
        )

    def from_parents(self, parent1: Agent, parent2: Agent) -> Agent:
        child_genes = AgentInputs.from_parents(parent1, parent2)
        return self.build(child_genes)

    def initialize_random(self) -> Agent:
        inputs = AgentInputs.init_random()
        return self.build(inputs)

    def create_generation_from_best_agents(
        self, best_agents: list[Agent], no_of_agents: int
    ):
        pairs = create_n_pairs_from_elements(best_agents, no_of_agents)

        return [self.from_parents(*parents) for parents in pairs]
