# A/B Testing

## About

A/B Tests for the following two datasets:
- [Fast Food Marketing Campaign](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test) from Kaggle: A/B test of marketing variants measuring conversion/revenue. 

**Scenario:**
A fast-food chain plans to add a new item to its menu. However, they are still undecided between three possible marketing campaigns for promoting the new product. In order to determine which promotion has the greatest effect on sales, the new item is introduced at locations in several randomly selected markets. A different promotion is used at each location, and the weekly sales of the new item are recorded for the first four weeks. 
The relevant information is included in the dataset, which we'll explore.

**Goal:**
Evaluate A/B testing results and decide which marketing strategy works the best.

**Target Metric:**
Average weekly sales per location

- [Cookie Cats](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats) from Kaggle: A/B test moving the first gate from level 30 to 40; evaluate day‑1/day‑7 retention and engagement.

This dataset includes A/B test results of Cookie Cats to examine what happens when the first gate in the game was moved from level 30 to level 40. When a player installed the game, he or she was randomly assigned to either gate_30 or gate_40.

The data we have is from 90,189 players that installed the game while the AB-test was running.

**Goal:**
Evaluate A/B testing results and decide whether to set the gate to 30 or 40.

**Target Metric:**
0.1 * retention_1 + 0.7 * retention_7 + 0.2 * (sum_gamerounds - min)/(max - min)
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