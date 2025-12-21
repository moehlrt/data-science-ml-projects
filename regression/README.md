# DS.v3.2.3.4

## About

This project performs a regression analysis on the "Vinho Verde" wine quality dataset. The goal is to understand which physicochemical properties (like acidity, sugar, alcohol, etc.) influence the sensory quality ratings of red wine.

The analysis includes:
- **Exploratory Data Analysis (EDA):** Correlation analysis and data cleaning.
- **Hypothesis Testing:** Investigating relationships between chemical properties and quality.
- **Linear Regression Modeling:** Predicting wine quality based on physicochemical features.
- **Model Evaluation:** Interpreting coefficients and checking statistical significance.

**Dataset:**
- [Red Wine Quality](https://archive.ics.uci.edu/ml/datasets/wine+quality) (Cortez et al., 2009).

## Repository Structure

```text
├── consts.py                   # Constants and configuration
├── utils.py                    # Utils/ Helper functions
├── wine_quality_analysis.ipynb # Main analysis notebook
├── Datasets/
│   ├── winequality-red.csv
│   └── winequality-red-copy.csv
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── 234.md                      
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
2) Open `wine_quality_analysis.ipynb` in Jupyter.
3) Run all cells (Kernel → Restart & Run All). Adjust dataset paths if needed.

## Author

Moritz Ehlert
