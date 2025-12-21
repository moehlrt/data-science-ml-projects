# DS.v3.1.4.5
## About

This repository contains a data cleaning and exploratory data analysis project on Coursera courses. The central guiding question is: "What makes a course successful?" We define a composite success metric and evaluate multiple factors such as geography, certificate type, difficulty level, organization, and subject area.

Dataset: Kaggle – `Coursera Course Dataset` [link referenced inside the notebook].

*To access all the visualizations I'd  propose to open the notebook via the following google colab link due to the use of plotly visualizations:* 

https://colab.research.google.com/drive/1KM0WdAYhEKvRYzRMncQoSmqdKGfuNGBU?usp=sharing

## Repository Structure

- `Data_Analysis/`
  - `Coursera_Analysis.ipynb`: Main notebook with cleaning, EDA, visualizations, hypotheses and conclusions
  - `funcs.py`: Helper functions (data prep, comparisons, categorization)
  - `consts.py`: Constants and mappings (paths, country/continent mappings, etc.)
- `Dataset/`
  - `coursera_data.csv`: Raw dataset
  - `coursera_data_processed.csv`: Exported processed dataset

## Setup

1) Python 3.10+ recommended
2) Install imported packages.
3) Jupyter environment (Notebook or JupyterLab).

## How to Run

1) Open `Data_Analysis/Coursera_Analysis.ipynb`
2) Run all cells top-to-bottom
   - Data cleaning and validation
   - Success Score creation
   - Hypotheses H1–H5 with plots and conclusions
   - Export of `coursera_data_processed.csv`

If paths differ on your machine, update them in `consts.py`.

## Further Notes

- The notebook uses Plotly for interactive visualizations; ensure internet access or a recent Plotly version.
- Bayesian shrinkage is applied for country-level success scores to stabilize small-sample regions.
