## About

1\. Perform exploratory data analysis. This should include creating statistical summaries and charts, testing for anomalies, and checking for correlations and other relations between variables and other EDA elements.

2\. Perform statistical inference. This should include defining the target population, forming multiple statistical hypotheses and constructing confidence intervals, setting the significance levels, and conducting z or t-tests for these hypotheses.

3\. Build generic time-series model that is capable of predicting next day stock price based on previous patterns. Note: the model should be the same for all stocks. Evaluate its performance on each stock independently.

4\. Using survival analysis methods, train models that are capable of predicting time to event (in this case event is ≥5% daily increase in stock price). Note: the model should be the same for all stocks. Evaluate its performance on each stock independently.

5\. Build ranking model that is capable of ranking given stocks in descending order in terms of possible daily gains from each stock.

Dataset: Daily granularity data for Apple (AAPL), Microsoft (MSFT), Amazon (AMZN), Google (GOOGL), Meta (META) stocks from 2010 to this date. You can find the dataset [here](https://pypi.org/project/yfinance/).

## Repository Structure

```text
├── .gitignore            # Git ignore rules
├── 335.md                # Project notes
├── README.md             # Project documentation
├── requirements.txt      # Dependencies
└── yfinance.ipynb        # Main notebook
```

## Getting Started

### Setup
1) Python 3.10+ recommended
2) Create a virtual environment
3) Install dependencies from `requirements.txt`
4) Jupyter Notebook installed

### Installing

Clone the repository and set up a virtual environment:
```bash
git clone <REPO_URL>
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

### Executing program

1) Start Jupyter notebook
2) Open `yfinance.ipynb` in Jupyter.
3) Run all cells. Adjust dataset paths if needed.

## Author

Moritz Ehlert