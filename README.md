# FourthDownIQ

### AI-Powered Fourth Down Decision Intelligence

FourthDownIQ is an AI/ML-powered football analytics platform that helps evaluate fourth-down situations and recommends the optimal decision: **GO, PUNT, or FIELD GOAL**.

Instead of relying only on traditional football intuition, FourthDownIQ analyzes the game context and provides a data-driven recommendation with probabilities, confidence, and model insights.

---

## Overview

A fourth-down decision can completely change the outcome of a football game.

FourthDownIQ takes a game situation such as:

* Yards to go
* Field position
* Score differential
* Time remaining
* Distance category
* Field zone
* Score state
* Time state

and sends these features to a trained machine-learning model.

The system then predicts the probabilities of:

**GO vs PUNT vs FIELD GOAL**

and identifies the recommended decision.

---

## Features

### AI Decision Analyzer

Enter a real game situation and receive an ML-powered recommendation.

The analyzer provides:

* Recommended decision
* Prediction confidence
* GO probability
* PUNT probability
* FIELD GOAL probability
* Human-readable explanation
* Model factors influencing the prediction

### Interactive Game Simulator

Experiment with different game situations using interactive controls.

Change:

* Yards to go
* Yard line
* Score differential
* Time remaining
* Distance group
* Field zone

and see how the recommended decision changes.

### Scenario Presets

FourthDownIQ includes predefined scenarios for quickly testing common situations:

* Short Yardage
* Fourth & Long
* Field Goal Range
* Two-Minute Drill
* Goal Line

### Analysis History

Previous predictions are stored locally in the browser.

The history shows:

* Game situation
* Timestamp
* Recommendation
* Confidence
* Score differential
* Time remaining

Users can also clear their analysis history.

### Model Insights

FourthDownIQ goes beyond simply giving a prediction.

The platform displays the factors that influenced the model's decision, helping users understand **why** a particular decision was recommended.

### Dark / Light Mode

The interface supports both dark and light themes, with the selected theme saved locally.

### Responsive Interface

The frontend is designed to work across:

* Desktop
* Tablet
* Mobile

---

## How It Works

```text
User enters game situation
          ↓
Frontend validates inputs
          ↓
Request sent to FastAPI backend
          ↓
Machine Learning Model
          ↓
GO / PUNT / FIELD GOAL probabilities
          ↓
Recommended decision
          ↓
Confidence + Model Insights
          ↓
Result displayed in dashboard
```

---

## Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI
* LocalStorage

### Backend

* Python
* FastAPI
* Uvicorn

### Machine Learning

* Python
* Scikit-learn
* Pandas
* NumPy

### Data

The model is trained using historical NFL play-by-play data and engineered game-state features.

---

## Input Features

| Feature                  | Description                        |
| ------------------------ | ---------------------------------- |
| `ydstogo`                | Yards required for a first down    |
| `yardline_100`           | Distance from opponent's goal line |
| `score_differential`     | Current score difference           |
| `game_seconds_remaining` | Time remaining in the game         |
| `distance_group`         | Short / Medium / Long              |
| `field_zone`             | Field position category            |
| `score_state`            | Winning / Losing / Tied            |
| `time_state`             | Normal / Late / Critical           |

---

## Prediction Output

The model returns a structure similar to:

```json
{
  "recommended_decision": "GO",
  "confidence": 72.45,
  "probabilities": {
    "GO": 72.45,
    "PUNT": 18.21,
    "FIELD_GOAL": 9.34
  }
}
```

The frontend converts these predictions into an interactive visual result.

---

## Project Structure

```text
FourthDownIQ/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   └── ...
│
├── models/
│   └── trained_models
│
├── data/
│   └── dataset
│
├── train_models.py
│
└── README.md
```

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FourthDownIQ.git
cd FourthDownIQ
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the FastAPI backend

```bash
uvicorn app:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

### 4. Open the frontend

Open:

```text
frontend/index.html
```

in your browser.

Make sure the frontend API URL points to your running backend.

---

## API Endpoint

### `POST /predict`

The prediction endpoint accepts game-state information and returns the recommended fourth-down decision.

Example request:

```json
{
  "ydstogo": 4,
  "yardline_100": 45,
  "score_differential": 0,
  "game_seconds_remaining": 300,
  "distance_group": "medium",
  "field_zone": "midfield",
  "score_state": "tied",
  "time_state": "normal"
}
```

---

## Why FourthDownIQ?

Traditional fourth-down decisions can depend heavily on intuition, coaching philosophy, and game pressure.

FourthDownIQ provides another perspective:

> **Turn a game situation into a data-driven decision.**

The goal isn't to replace coaches or analysts.

The goal is to provide an intelligent analytical signal that can help users understand the strategic trade-offs behind fourth-down decisions.

---

## Future Improvements

Potential future additions include:

* Live NFL game integration
* Real-time fourth-down alerts
* Team-specific decision models
* Expected Points Added (EPA)
* Win Probability
* Weather conditions
* Opponent strength
* Coach decision tendencies
* Advanced explainable AI
* Interactive game timeline
* Model comparison
* Cloud-based analysis history

---

## Disclaimer

FourthDownIQ is an educational and experimental sports analytics project.

Predictions are generated using machine-learning models trained on historical data and should not be considered guaranteed outcomes or professional coaching advice.

---

## Project Status

**Active Development**

FourthDownIQ is being developed as an AI/ML sports analytics project focused on combining machine learning, football strategy, and interactive data visualization.

---

## Author

**Eesha Mishra**

B.Tech CSE (AI & ML)

---

## License

This project is intended for educational and research purposes.
