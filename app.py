from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from predict import predict_decision


# ============================================================
# FOURTHDOWNIQ — FASTAPI BACKEND
# ============================================================

app = FastAPI(
    title="FourthDownIQ API",
    description="NFL Fourth-Down Decision Prediction API",
    version="1.0.0"
)


# ============================================================
# CORS — ALLOW FRONTEND TO CONNECT
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# INPUT DATA MODEL
# ============================================================

class FourthDownSituation(BaseModel):

    ydstogo: float

    yardline_100: float

    score_differential: float

    game_seconds_remaining: float

    distance_group: str

    field_zone: str

    score_state: str

    time_state: str


# ============================================================
# HOME ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "project": "FourthDownIQ",
        "status": "online",
        "message": "NFL Fourth-Down Decision Prediction API"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(situation: FourthDownSituation):

    result = predict_decision(

        ydstogo=situation.ydstogo,

        yardline_100=situation.yardline_100,

        score_differential=situation.score_differential,

        game_seconds_remaining=situation.game_seconds_remaining,

        distance_group=situation.distance_group,

        field_zone=situation.field_zone,

        score_state=situation.score_state,

        time_state=situation.time_state
    )

    return result