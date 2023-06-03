import os

"""
I assume that after 2 years people do not remember brands. No data to back that up
"""
CONSUMER_RECALL = 24
SHORT_CONSUMER_RECALL = 2

DataAggregatorProps = {
    "stock_prices": os.path.join("data", "stock_prices.csv"),
    "opinions": os.path.join("data", "trends.csv"),
    "stock_trends": os.path.join("data", "stock_trends.csv"),
}

FIELDS_TO_MUTATE = 10
MUTATION_FACTOR = 0.5

COMPANY_BIAS_INFLUENCE = 0.3
SECTOR_BIAS_INFLUENCE = 0.2

SimulationProps = {
    "number_of_agents": 300,
    "agent_life_expectancy": 2 * 12,
    "delta": 6,
    "num_of_best_candidates": 40,
    "start_date": (6, 2010),
    "end_date": (5, 2023),
}

AgentBuilderProps = {
    "start_balance": 10_000,
    "min_transaction": 10,
    "max_transaction": 5000,
}

TRANSACTION_FEE = 10
DIVERSIFICATION_BONUS = 10
