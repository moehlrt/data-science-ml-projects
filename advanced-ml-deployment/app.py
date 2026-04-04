from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="Portugal Real Estate Price Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myfrontend.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept", "X-API-Key"],
)

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return api_key

model = joblib.load("model/model.pkl")
feature_info = joblib.load("model/feature_info.pkl")

class PropertyFeatures(BaseModel):
    District: str
    Type: str
    EnergyCertificate: str
    TotalArea: float
    Parking: float
    ConstructionYear: float
    Elevator: int
    LivingArea: float
    NumberOfBathrooms: float

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: PropertyFeatures, api_key: str = Depends(verify_api_key)):
    input_df = pd.DataFrame([data.model_dump()])

    for col in feature_info["all_columns"]:
        if col not in input_df.columns:
            input_df[col] = np.nan

    input_df = input_df[feature_info["all_columns"]]

    log_pred = model.predict(input_df)[0]
    price_pred = float(np.expm1(log_pred))

    return {
        "predicted_price_eur": round(price_pred, 2),
        "log_prediction": round(float(log_pred), 4),
    }