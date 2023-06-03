from genetic_algorithm_stock_prediction.agent import Agent
from genetic_algorithm_stock_prediction.constants import SimulationProps
from genetic_algorithm_stock_prediction.model import StockGeneticAlgorithmModel


def display_best_children_stats(children: list[Agent]):
    for agent in children:
        agent.show_stats()


def run():
    model = StockGeneticAlgorithmModel(**SimulationProps)
    model.initialize()

    model.run_training()

    best_agents = model.get_best_agents()

    model.create_best_agents_summary()

    report = best_agents[0].get_report()
    print("BEST AGENT")
    print(report)

