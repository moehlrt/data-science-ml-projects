# Tech Industry Mental Health Analysis

## About

In this notebook we will be exploring the [coursera dataset](https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry/data) from kaggle, which is about Mental Health in the Tech industry.
In the main notebook we defined a guiding question and iteratively raised hypotheses to come to a conclusion.

- Main artefact: `Mental_Health_Data.ipynb`
- Database: SQLite (`Dataset/mental_health.sqlite`), duplicated to `Dataset/mental_health_copy.sqlite` for safe experimentation

## Repository Structure

```
├── Analysis/
│   ├── answer_check.py                       
│   ├── consts.py                             # DB path as const
│   └── Queries/                              # All Queries categorized by Influence in Analysis
│       ├── single_diseases_query.py          
│       ├── sociodemograhic_queries.py        
│       ├── sociodemograhic_influence_queries.py 
│       ├── workplace_influence_queries.py    
│       └── social_influence_queries.py       
├── Dataset/
│   ├── mental_health.sqlite                  # Main SQLite DB
│   └── mental_health_copy.sqlite             # Auto-created working copy
|── Mental_Health_Analysis.ipynb                  # Main notebook
├── README.md
├── requirements.txt            
└── 215.md
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

2) Open `Mental_Health_Data.ipynb` and run the setup cells. The database copy/connect snippet 

3) Execute the analysis cells section by section. SQL queries live under `Analysis/Queries/`.

## Author

Moritz Ehlert