import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    log_loss,
    brier_score_loss
)


# ============================================================
# STEP 1 — LOAD DATASET
# ============================================================

df = pd.read_csv("fourth_down_ml.csv")

print("=" * 70)
print("FOURTHDOWNIQ — MODEL TRAINING")
print("=" * 70)

print("\nDataset loaded!")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nDecision distribution:")
print(df["decision"].value_counts())

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# STEP 2 — FEATURES AND TARGET
# ============================================================

features = [
    "ydstogo",
    "yardline_100",
    "score_differential",
    "game_seconds_remaining",
    "distance_group",
    "field_zone",
    "score_state",
    "time_state"
]

X = df[features]
y = df["decision"]


# ============================================================
# STEP 3 — FEATURE TYPES
# ============================================================

categorical_features = [
    "distance_group",
    "field_zone",
    "score_state",
    "time_state"
]

numerical_features = [
    "ydstogo",
    "yardline_100",
    "score_differential",
    "game_seconds_remaining"
]


# ============================================================
# STEP 4 — PREPROCESSING
# ============================================================

# For Logistic Regression
preprocessor_scaled = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)


# For Decision Tree / Random Forest
preprocessor_tree = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

print("\nPreprocessing systems created successfully!")


# ============================================================
# STEP 5 — TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n" + "=" * 70)
print("TRAIN / TEST SPLIT")
print("=" * 70)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# STEP 6 — LOGISTIC REGRESSION
# ============================================================

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor_scaled),
        (
            "model",
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced"
            )
        )
    ]
)

print("\n" + "=" * 70)
print("LOGISTIC REGRESSION")
print("=" * 70)

logistic_model.fit(X_train, y_train)

logistic_predictions = logistic_model.predict(X_test)

logistic_accuracy = accuracy_score(
    y_test,
    logistic_predictions
)

print("\nAccuracy:")
print(f"{logistic_accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        logistic_predictions,
        zero_division=0
    )
)


# ============================================================
# STEP 7 — DECISION TREE
# ============================================================

decision_tree_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor_tree),
        (
            "model",
            DecisionTreeClassifier(
                max_depth=6,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)

print("\n" + "=" * 70)
print("DECISION TREE")
print("=" * 70)

decision_tree_model.fit(X_train, y_train)

tree_predictions = decision_tree_model.predict(X_test)

tree_accuracy = accuracy_score(
    y_test,
    tree_predictions
)

print("\nAccuracy:")
print(f"{tree_accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        tree_predictions,
        zero_division=0
    )
)


# ============================================================
# STEP 8 — BASELINE RANDOM FOREST
# ============================================================

random_forest_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor_tree),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1
            )
        )
    ]
)

print("\n" + "=" * 70)
print("BASELINE RANDOM FOREST")
print("=" * 70)

random_forest_model.fit(X_train, y_train)

rf_predictions = random_forest_model.predict(X_test)

rf_accuracy = accuracy_score(
    y_test,
    rf_predictions
)

print("\nAccuracy:")
print(f"{rf_accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        rf_predictions,
        zero_division=0
    )
)


# ============================================================
# STEP 9 — RANDOM FOREST HYPERPARAMETER TUNING
# ============================================================

print("\n" + "=" * 70)
print("RANDOM FOREST HYPERPARAMETER TUNING")
print("=" * 70)

tuning_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor_tree),
        (
            "model",
            RandomForestClassifier(
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


param_distributions = {
    "model__n_estimators": [
        200,
        300,
        500,
        700
    ],

    "model__max_depth": [
        None,
        10,
        15,
        20,
        25,
        30
    ],

    "model__min_samples_split": [
        2,
        5,
        10
    ],

    "model__min_samples_leaf": [
        1,
        2,
        4
    ],

    "model__max_features": [
        "sqrt",
        "log2",
        None
    ],

    "model__class_weight": [
        "balanced",
        "balanced_subsample"
    ]
}


random_search = RandomizedSearchCV(
    estimator=tuning_pipeline,
    param_distributions=param_distributions,
    n_iter=30,
    cv=5,
    scoring="f1_macro",
    random_state=42,
    n_jobs=-1,
    verbose=1
)

print("\nStarting hyperparameter search...")
print("Testing 30 combinations with 5-fold CV.")
print("This may take a few minutes.\n")

random_search.fit(
    X_train,
    y_train
)

print("\nHyperparameter tuning completed!")


# ============================================================
# STEP 10 — BEST PARAMETERS
# ============================================================

print("\n" + "=" * 70)
print("BEST RANDOM FOREST PARAMETERS")
print("=" * 70)

print("\nBest Parameters:")

for parameter, value in random_search.best_params_.items():
    print(f"{parameter}: {value}")

print("\nBest 5-Fold Cross-Validation Macro F1:")
print(
    f"{random_search.best_score_ * 100:.2f}%"
)


# ============================================================
# STEP 11 — TUNED RANDOM FOREST
# ============================================================

tuned_rf_model = random_search.best_estimator_

tuned_predictions = tuned_rf_model.predict(
    X_test
)

tuned_accuracy = accuracy_score(
    y_test,
    tuned_predictions
)

print("\n" + "=" * 70)
print("TUNED RANDOM FOREST")
print("=" * 70)

print("\nTest Accuracy:")
print(
    f"{tuned_accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        tuned_predictions,
        zero_division=0
    )
)


# ============================================================
# STEP 12 — CONFUSION MATRIX
# ============================================================

tuned_cm = confusion_matrix(
    y_test,
    tuned_predictions,
    labels=[
        "PUNT",
        "FIELD_GOAL",
        "GO"
    ]
)

print("\nConfusion Matrix:")

print(tuned_cm)

print("\nLabels:")
print([
    "PUNT",
    "FIELD_GOAL",
    "GO"
])


# ============================================================
# STEP 13 — PROBABILITY CALIBRATION
# ============================================================

print("\n" + "=" * 70)
print("PROBABILITY CALIBRATION")
print("=" * 70)

print("\nCalibrating the tuned Random Forest...")
print("This may take a little time.\n")


calibrated_rf_model = CalibratedClassifierCV(
    estimator=tuned_rf_model,
    method="sigmoid",
    cv=5,
    n_jobs=-1
)

calibrated_rf_model.fit(
    X_train,
    y_train
)

print("Probability calibration completed!")


# ============================================================
# STEP 14 — CALIBRATED PREDICTIONS
# ============================================================

calibrated_predictions = calibrated_rf_model.predict(
    X_test
)

calibrated_probabilities = (
    calibrated_rf_model.predict_proba(
        X_test
    )
)

calibrated_accuracy = accuracy_score(
    y_test,
    calibrated_predictions
)

print("\nCalibrated Model Accuracy:")
print(
    f"{calibrated_accuracy * 100:.2f}%"
)

print("\nCalibrated Classification Report:")

print(
    classification_report(
        y_test,
        calibrated_predictions,
        zero_division=0
    )
)


# ============================================================
# STEP 15 — CALIBRATED PROBABILITY EVALUATION
# ============================================================

print("\n" + "=" * 70)
print("PROBABILITY QUALITY")
print("=" * 70)

calibrated_logloss = log_loss(
    y_test,
    calibrated_probabilities,
    labels=calibrated_rf_model.classes_
)

print("\nCalibrated Log Loss:")
print(
    f"{calibrated_logloss:.4f}"
)

print(
    "\nLower Log Loss = better probability predictions."
)


# ============================================================
# STEP 16 — SHOW PROBABILITIES
# ============================================================

print("\n" + "=" * 70)
print("CALIBRATED PROBABILITY PREDICTIONS")
print("=" * 70)

class_names = calibrated_rf_model.classes_

print("\nClass order:")
print(class_names)

print("\nFirst 20 predictions:\n")

for i in range(20):

    print(f"Example {i + 1}")

    for class_name, probability in zip(
        class_names,
        calibrated_probabilities[i]
    ):

        print(
            f"  {class_name}: "
            f"{probability * 100:.2f}%"
        )

    print(
        f"  Recommended: "
        f"{calibrated_predictions[i]}"
    )

    print("-" * 40)


# ============================================================
# STEP 17 — FEATURE IMPORTANCE
# ============================================================

print("\n" + "=" * 70)
print("TUNED RANDOM FOREST FEATURE IMPORTANCE")
print("=" * 70)

rf_model = tuned_rf_model.named_steps["model"]

feature_names = (
    tuned_rf_model
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

importances = rf_model.feature_importances_

feature_importance = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
})

feature_importance = (
    feature_importance
    .sort_values(
        by="importance",
        ascending=False
    )
)

print(
    feature_importance.to_string(
        index=False
    )
)


# ============================================================
# STEP 18 — FINAL MODEL COMPARISON
# ============================================================

print("\n" + "=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)

print("\nAccuracy:")

print(
    f"Logistic Regression      : "
    f"{logistic_accuracy * 100:.2f}%"
)

print(
    f"Decision Tree            : "
    f"{tree_accuracy * 100:.2f}%"
)

print(
    f"Baseline Random Forest   : "
    f"{rf_accuracy * 100:.2f}%"
)

print(
    f"Tuned Random Forest      : "
    f"{tuned_accuracy * 100:.2f}%"
)

print(
    f"Calibrated Random Forest : "
    f"{calibrated_accuracy * 100:.2f}%"
)


print("\nCross-Validation:")

print(
    f"Tuned RF 5-Fold Macro F1 : "
    f"{random_search.best_score_ * 100:.2f}%"
)


# ============================================================
# STEP 19 — FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FOURTHDOWNIQ — FINAL SUMMARY")
print("=" * 70)

print("\nBest classification model:")
print("Tuned Random Forest")

print(
    f"\nTest Accuracy: "
    f"{tuned_accuracy * 100:.2f}%"
)

print(
    f"5-Fold CV Macro F1: "
    f"{random_search.best_score_ * 100:.2f}%"
)

print(
    f"Calibrated Log Loss: "
    f"{calibrated_logloss:.4f}"
)

print("\nDecision Classes:")
print("PUNT")
print("FIELD_GOAL")
print("GO")

print("\nTraining completed successfully!")
print("=" * 70)
# ============================================================
# STEP 20 — SAVE TRAINED MODEL
# ============================================================

import joblib

model_filename = "fourthdowniq_model.joblib"

joblib.dump(
    calibrated_rf_model,
    model_filename
)

print("\nModel saved successfully!")
print(f"Saved as: {model_filename}")