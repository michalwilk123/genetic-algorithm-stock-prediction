from .agent import Agent, AgentBuilder
from .constants import AgentBuilderProps, DataAggregatorProps
from .data_aggregator import DataAggregator, Month, Year
from .utils import calculate_next_date, create_month_year_generator


class StockGeneticAlgorithmModel:
    def __init__(
        self,
        *,
        number_of_agents: int,
        agent_life_expectancy: int,
        delta: int,
        num_of_best_candidates: int,
        start_date: tuple[int, int],
        end_date: tuple[int, int]
    ) -> None:
        self._number_of_agents = number_of_agents
        self._time_to_live = agent_life_expectancy
        self._delta = delta
        self._num_of_best_candidates = num_of_best_candidates
        self._start = start_date
        self._end = end_date

    def initialize(self):
        self._data_aggregator = DataAggregator(**DataAggregatorProps)
        self._agent_builder = AgentBuilder(
            **AgentBuilderProps, data_aggregator=self._data_aggregator
        )

        self._agents: list[Agent] = [
            self._agent_builder.initialize_random()
            for _ in range(self._number_of_agents)
        ]
        self._agent_history = [self._agents]
        self._results = []

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

        results = [agent.evaulate() for agent in self._agents]
        self._results.append(results)

        best_candidates = sorted(self._agents, key=lambda agent: agent.evaluate())[
            : self._num_of_best_candidates : -1
        ]

        new_generation = self._agent_builder.create_generation_from_best_agents(
            best_candidates, self._number_of_agents
        )

        self._agent_history.append(new_generation)
        self._agents = new_generation

    def run_training(self):
        current_delta = 0

        actual_end = calculate_next_date(self._end, -self._time_to_live)

        for month, year in create_month_year_generator(self._start, actual_end):
            if current_delta >= self._delta:
                self.run_epoch(month, year)
                current_delta = 0
                continue

            current_delta += 1
