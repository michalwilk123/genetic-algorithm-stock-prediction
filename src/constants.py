import logging
from pathlib import Path
from typing import NamedTuple

"""
I assume that after 2 years people do not remember brands. No data to back that up
"""
CONSUMER_RECALL = 24
SHORT_CONSUMER_RECALL = 2


class DataAggregatorProps(NamedTuple):
    stock_prices: str = str(Path("data") / "stock_prices.csv")
    opinions: str = str(Path("data") / "trends.csv")
    stock_trends: str = str(Path("data") / "stock_trends.csv")


MUTATION = 0.3
FIELDS_TO_MUTATE = 4


class SimulationProps(NamedTuple):
    number_of_agents: int = 10
    agent_life_expectancy: int = 3 * 12
    delta = 2
    start_date: tuple[int, int] = (6, 2020)
    end_date: tuple[int, int] = (6, 2010)


LOG_LEVEL = logging.INFO


class AgentBuilderProps(NamedTuple):
    start_balance: int = 10_000
    min_transaction: int = 10
    max_transaction: int = 5000
