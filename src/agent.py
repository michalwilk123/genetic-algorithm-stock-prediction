from typing import NamedTuple

from .data_aggregator import CompanyData

class AgentInputs(NamedTuple):
    courage: float
    amount_multiplier: float

    stock_trend_bias: float
    trend_bias: float

    stock_trend_velocity_bias: float
    trend_velocity_bias: float

    sector_bias: float
    company_bias: float

class Agent:
    def __init__(self) -> None:
        pass

    @classmethod
    def from_parent(cls):
        ...

    @classmethod
    def initialize_random(cls):
        ...

    def make_decision(self, company_data:CompanyData):
        ...


    def create_genes(self):
        ...
