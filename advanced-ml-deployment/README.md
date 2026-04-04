## About

The primary objective of the project is to create a machine learning model, which could predict the price for a given house in Portugal given some data.

**1.** We perform exploratory data analysis. This includes creating statistical summaries and charts, testing for anomalies, checking for correlations and other relations between variables, and other EDA elements.

**2.** We perform statistical inference. This includes defining the target population, forming multiple statistical hypotheses and constructing confidence intervals, setting the significance levels, conducting z or t-tests for these hypotheses.

**3.** Apply various machine learning models to predict the "price" column using all other features. This should include hyperparameter tuning, model ensembling, the analysis of model selection, and other methods.

**4.** Deploy the machine learning model. Choose the best performing model and deploy it. You are free to choose any deployment option that you like - you need to containerize the model as a service application and deploy it to Google Cloud Platform so that the model output could be callable through HTTP request.

**Dataset:**
- [Real Estate Listings in Portugal](https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024)

**Context:**

This weekly updated dataset contains the more than 100k real asking prices for real estate properties listed on Portuguese real estate websites. The data was legally and ethically scraped from several online platforms, ensuring compliance with the platforms' terms and conditions.

## Repository Structure

```text
├── .gcloudignore                       # Google Cloud ignore rules
├── .gitignore                          # Git ignore rules
├── 325.md                              # Project notes
├── Dockerfile                          # Container setup
├── README.md                           # Project documentation
├── app.py                              # App entry point
├── consts.py                           # Constants
├── datasets/
│   ├── portugal_listings.csv
│   └── portugal_listings_copy.csv
├── model/
│   ├── feature_info.pkl               # Model metadata
│   └── model.pkl                      # Trained model
├── realestate-price-prediction.ipynb   # Main notebook
└── requirements.txt                    # Dependencies
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
2) Open `realestate-price-prediction.ipynb` in Jupyter.
3) Run all cells. Adjust dataset paths if needed.

### Running the API

**Locally (without Docker):**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Locally via Docker:**
```bash
docker build -t realestate-api .
docker run -p 8000:8080 realestate-api
```

The API exposes:
- `POST /predict` — predict property price (requires `X-API-Key` header)
- `GET /health` — health check

### Deployment (Google Cloud Run)

The model is containerized via Docker and deployed to Google Cloud Run. The Dockerfile packages the FastAPI app, the trained model, and all dependencies into a Docker image. This image is built on Google Cloud Build, pushed to Google Container Registry, and then deployed as a managed service on Cloud Run.

**Base URL:** `https://realestate-api-826068099925.europe-west1.run.app`

**Test the deployed API:**
```bash
curl https://realestate-api-826068099925.europe-west1.run.app/health
```

```bash
curl -X POST https://realestate-api-826068099925.europe-west1.run.app/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: my-secret-key" \
  -d '{"District":"Lisboa","Type":"Apartment","EnergyCertificate":"B","TotalArea":100,"Parking":1,"ConstructionYear":2010,"Elevator":1,"LivingArea":80,"NumberOfBathrooms":2}'
```

**Redeploying after changes:**
```bash
gcloud builds submit --tag gcr.io/turing-college-491711/realestate-api
gcloud run deploy realestate-api --image gcr.io/turing-college-491711/realestate-api --platform managed --region europe-west1 --allow-unauthenticated --port 8080
```

For Ensemble: 

```bash
gcloud run deploy realestate-api --image gcr.io/turing-college-491711/realestate-api --platform managed --region europe-west1 --allow-unauthenticated --port 8080 --memory 4Gi --cpu 2 --cpu-boost 
```

**Delete the deployment:**
```bash
gcloud run services delete realestate-api --region europe-west1
```

## Author

Moritz Ehlert