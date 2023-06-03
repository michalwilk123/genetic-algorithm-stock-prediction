from pprint import pprint

from genetic_algorithm_stock_prediction.agent import Agent
from genetic_algorithm_stock_prediction.constants import SimulationProps
from genetic_algorithm_stock_prediction.model import StockGeneticAlgorithmModel
from genetic_algorithm_stock_prediction.utils import (
    calculate_next_date,
    create_month_year_generator,
)


def display_best_children_stats(children: list[Agent]):
    for agent in children:
        agent.show_stats()


def run():
    model = StockGeneticAlgorithmModel(**SimulationProps)
    model.initialize()

    model.run_training()
    model.show_agents_summary()

    best_agent = model.get_best_agents()[0]
    current_date = (5, 2023)

    for month, year in create_month_year_generator(
        calculate_next_date(current_date, -SimulationProps["delta"]), current_date
    ):
        best_agent.run_month(month, year)

    best_agent.close_positions(*current_date)
    report = best_agent.get_report()

    print("BEST AGENT:")
    pprint(report)
