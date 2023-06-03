### Implementation of genetic algorithm in python in stock market prediction

In this project i implemented naive genetic algorithm that learns from the available
Google Trends data i scraped from the internet. I used also Yahoo to fetch stock prices.

The model tracks some features like the brand popularity, stock popularity
and then applies this knowledge for predicting what stock to buy by what amount.

Each agent has bias towards trends, companies, sectors as well as many more biases (aprox. 60 weights)

The _report.txt_ file contains results from the bot from 06-2010 to 06-2023

The project was made for educational purposes as a project for Machine Learning Methods
class in Gdańsk University of Technology.


The result of the training was this agent:
```python
AgentReport(profit=(396.7624472728585,),
            number_of_transactions=9,
            average_transaction_amount=2259.6402719192065,
            multiplier=0.30722326771436814,
            courage=0.5518224612738823,
            invested_companies=3,
            sector_biases={'AUTOMOTIVE': 0.4945335353859816,
                           'BANKING': 0.5160124180318092,
                           'ENERGY': 0.7505727618903173,
                           'FOOD': 0.5001275936823805,
                           'HEALTHCARE': 0.6685896409295591,
                           'MEDIA': 0.5532138072973746,
                           'RETAIL': 0.4889761815866155,
                           'SOFTWARE': 0.5232449605079104,
                           'TECHNOLOGY': 0.5500394773036379,
                           'TELECOMUNICATION': 0.5305580345668408},
            bought_stocks={'AAPL': 2611, 'MSFT': 3494, 'PFE': 3835})
```