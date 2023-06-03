import unittest

from genetic_algorithm_stock_prediction.agent import AgentBuilder, AgentInputs
from genetic_algorithm_stock_prediction.constants import FIELDS_TO_MUTATE, AgentBuilderProps, DataAggregatorProps
from genetic_algorithm_stock_prediction.data_aggregator import DataAggregator


class TestAgentInputs(unittest.TestCase):
    def test_crossover(self):
        parent1 = AgentInputs.init_random()
        parent2 = AgentInputs.init_random()

        child = AgentInputs.from_parents(parent1, parent2)

        parent_avg = (parent1.to_flat() + parent2.to_flat()) / 2

        n_of_mutations = 0

        for gen1, gen2 in zip(child.to_flat(), parent_avg):
            if gen1 != gen2:
                n_of_mutations += 1

            self.assertTrue(-1 <= gen1 <= 1)

        self.assertEqual(n_of_mutations, FIELDS_TO_MUTATE)

    def test_to_flat_conversion(self):
        inputs = AgentInputs.init_random()

        representation = inputs.to_flat()

        converted = AgentInputs.from_flat(representation)

        self.assertEqual(converted, inputs)

class TestAgent(unittest.TestCase):
    def test_happy_path(self):
        data_aggregator = DataAggregator(**DataAggregatorProps)
        agent_builder = AgentBuilder(**AgentBuilderProps, data_aggregator=data_aggregator)
        agent = agent_builder.initialize_random()

        agent.run_month(10, 2020)

        agent.close_positions()
        score = agent.evaluate()
