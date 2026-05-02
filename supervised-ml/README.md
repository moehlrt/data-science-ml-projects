## About

This project analyzes customer data to identify key factors influencing the purchase of travel insurance packages - based on our given dataset. We are also building a predictive classification model that identifies customers most likely to purchase the travel insurance package.

The analysis includes:
- **Exploratory Data Analysis (EDA):** Correlation analysis and data cleaning.
- **Hypothesis Testing:** Statistical validation of relationships using Welch’s t-tests (for numerical data) and Z-tests (for categorical data)
- **Modeling:** hyperparameter tuning, model ensembling, the analysis of model selection, and more.

**Dataset:**
- [Travel Insurance Prediction Data](https://www.kaggle.com/datasets/tejashvi14/travel-insurance-prediction-data)

## Repository Structure

```text
├── consts.py                   # Constants
├── ml-travel-insurance.ipynb   # Main notebook
├── datasets/
│   ├── TravelInsurancePrediction.csv
│   └── TravelInsurancePredictionCopy.csv
├── README.md                   # Project documentation
└── requirements.txt            # Dependencies                    
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
2) Open `ml-travel-insurance.ipynb` in Jupyter.
3) Run all cells (Kernel → Restart & Run All). Adjust dataset paths if needed.

## Author

Moritz Ehlert