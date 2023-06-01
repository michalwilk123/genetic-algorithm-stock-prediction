import constants

from .data_aggregator import DataAggregator


def main():
    data_aggregator = DataAggregator(
        constants.STOCK_PRICES_CSV_PATH,
        constants.TRENDS_CSV_PATH,
        constants.STOCK_TRENDS_CSV_PATH,
    )


if __name__ == "__main__":
    main()
