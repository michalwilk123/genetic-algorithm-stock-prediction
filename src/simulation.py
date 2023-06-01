from constants import DataAggregatorProps

from .agent import Agent, AgentBuilder
from .constants import DataAggregationProps
from .data_aggregator import DataAggregator, Month, Year
from .utils import calculate_next_date, create_month_year_generator


class StockGeneticAlgorithmModel:
    def __init__(
        self,
        *,
        number_of_agents: int,
        agent_life_expectancy: int,
        delta: int,
        start_date: tuple[int, int],
        end_date: tuple[int, int]
    ) -> None:
        self._number_of_agents = number_of_agents
        self._time_to_live = agent_life_expectancy
        self._delta = delta
        self._start = start_date
        self._end = end_date

    def initialize(self):
        self._agent_builder = AgentBuilder()
        self._data_aggregator = DataAggregator(**DataAggregatorProps)

        self._agents: list[Agent] = [
            Agent.initialize_random() for _ in range(self._number_of_agents)
        ]
        self._agent_history = [self._agents]

    def run_epoch(self, month: Month, year: Year):
        """
        Agents run in epochs that can overlap!
        Time to live defines how long each agent is playing
        before it is terminated.
        Delta defines the times between each agent start
        """
        start = (month, year)
        end = calculate_next_date(start, self._time_to_live)

        for month, year in create_month_year_generator(start, end):
            for agent in self._agents:
                agent.run_month(month, year)

    def run_training(self, data_aggregator: DataAggregator):
        current_delta = 0

        for month, year in create_month_year_generator(self._start, self._end):
            if current_delta >= self._delta:
                current_delta = 0
                continue

            self.run_epoch(month, year)

            current_delta += 1
