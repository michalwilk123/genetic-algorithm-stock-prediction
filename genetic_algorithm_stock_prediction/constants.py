import logging
from pathlib import Path

"""
I assume that after 2 years people do not remember brands. No data to back that up
"""
CONSUMER_RECALL = 24
SHORT_CONSUMER_RECALL = 2

DataAggregatorProps = {
    "stock_prices": str(Path("data") / "stock_prices.csv"),
    "opinions": str(Path("data") / "trends.csv"),
    "stock_trends": str(Path("data") / "stock_trends.csv"),
}

MUTATION = 0.3
FIELDS_TO_MUTATE = 4
MUTATION_FACTOR = 0.5

SimulationProps = {
    "number_of_agents": 10,
    "agent_life_expectancy": 1 * 12,
    "delta": 6,
    "num_of_best_candidates": 4,
    "start_date": (6, 2010),
    "end_date": (6, 2012),
}


LOG_LEVEL = logging.INFO

AgentBuilderProps = {
    "start_balance": 10_000,
    "min_transaction": 10,
    "max_transaction": 5000,
}

TRANSACTION_FEE = 10
DIVERSIFICATION_BONUS = 100
