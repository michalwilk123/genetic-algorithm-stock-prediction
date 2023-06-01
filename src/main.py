import constants
from agent import Agent
from simulation import StockGeneticAlgorithmModel

from .data_aggregator import DataAggregator


def display_best_children_stats(children: list[Agent]):
    for agent in children:
        agent.show_stats()


def main():
    simulation = StockGeneticAlgorithmModel(**constants.SimulationProps)
    simulation.initialize()

    simulation.run_training()

    best_agents = simulation.get_best_agents()

    display_best_children_stats(best_agents)


if __name__ == "__main__":
    main()
