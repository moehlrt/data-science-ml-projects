# DS.v3.2.2.5

## About

A/B Tests for the following two datasets:
- [Fast Food Marketing Campaign](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test) from Kaggle: A/B test of marketing variants measuring conversion/revenue.
- [Cookie Cats](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats) from Kaggle: A/B test moving the first gate from level 30 to 40; evaluate day‑1/day‑7 retention and engagement.

## Repository Structure

``` 
├── consts.py
├── fast_food_marketing_analysis.ipynb
├── game_cookie_cats_analysis.ipynb
└── Datasets/
    ├── cookie_cats.csv
    ├── cookie_cats_copy.csv
    ├── WA_Marketing-Campaign.csv
    └── WA_Marketing-Campaign_copy.csv
├── app.py
├── README.md
├── requirements.txt            
├── 225.md
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
2) Open the notebooks for each experiment (e.g., `game_cookie_cats_analysis.ipynb`, `fast_food_marketing_analysis.ipynb`).
3) Run all cells (Kernel → Restart & Run All). Adjust dataset paths if needed.
4) Optional dashboard (Fast Food Marketing Campaign):
   - Install extras: `pip install streamlit plotly`
   - Run: `streamlit run app.py`
   - Shows two plots: weekly target metric by promotion, and overall comparison with 95% CI.

## Author

Moritz Ehlert