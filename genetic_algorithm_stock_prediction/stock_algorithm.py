import dataclasses

# @dataclasses.dataclass
# class AgentInputs:


def buy_stock():
    ...


def calculate_decision():
    ...


def evaluate_agent(stock, stock_biases, balance, courage, multiplier):
    decision_value = calculate_decision()

    if -1 < decision_value * courage < 1:
        return

    cash_amount = decision_value * multiplier

    buy_stock(stock, cash_amount)
