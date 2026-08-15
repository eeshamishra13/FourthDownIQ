import joblib
import pandas as pd
import numpy as np
import shap


# ============================================================
# FOURTHDOWNIQ — LOAD MODEL
# ============================================================

MODEL_FILE = "fourthdowniq_model.joblib"

model = joblib.load(MODEL_FILE)

print("FourthDownIQ model loaded successfully!")


# ============================================================
# FEATURE DISPLAY NAMES
# ============================================================

FEATURE_DISPLAY_NAMES = {

    "numerical__ydstogo":
        "Yards to go",

    "numerical__yardline_100":
        "Field position",

    "numerical__score_differential":
        "Score differential",

    "numerical__game_seconds_remaining":
        "Time remaining",

    # Distance
    "categorical__distance_group_SHORT":
        "Short distance",

    "categorical__distance_group_MEDIUM":
        "Medium distance",

    "categorical__distance_group_LONG":
        "Long distance",

    "categorical__distance_group_VERY_LONG":
        "Very long distance",

    # Field zone
    "categorical__field_zone_OWN_TERRITORY":
        "Own territory",

    "categorical__field_zone_MIDFIELD":
        "Field position",

    "categorical__field_zone_OPPONENT_21_35":
        "Opponent territory",

    "categorical__field_zone_RED_ZONE":
        "Red zone",

    # Score
    "categorical__score_state_TRAILING":
        "Trailing",

    "categorical__score_state_TIED":
        "Game tied",

    "categorical__score_state_LEADING":
        "Leading",

    # Time
    "categorical__time_state_EARLY":
        "Early game",

    "categorical__time_state_MID":
        "Middle of game",

    "categorical__time_state_LATE":
        "Late game"
}


# ============================================================
# SHAP EXPLANATION
# ============================================================

def get_shap_explanation(input_data):

    # --------------------------------------------------------
    # Get preprocessing pipeline
    # --------------------------------------------------------

    preprocessor = (
        model
        .calibrated_classifiers_[0]
        .estimator
        .named_steps["preprocessor"]
    )

    # --------------------------------------------------------
    # Get Random Forest
    # --------------------------------------------------------

    rf_model = (
        model
        .calibrated_classifiers_[0]
        .estimator
        .named_steps["model"]
    )

    # --------------------------------------------------------
    # Transform input
    # --------------------------------------------------------

    transformed_input = preprocessor.transform(
        input_data
    )

    # --------------------------------------------------------
    # Feature names
    # --------------------------------------------------------

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    # --------------------------------------------------------
    # SHAP Tree Explainer
    # --------------------------------------------------------

    explainer = shap.TreeExplainer(
        rf_model
    )

    shap_values = explainer.shap_values(
        transformed_input
    )

    # --------------------------------------------------------
    # Determine predicted class
    # --------------------------------------------------------

    prediction = model.predict(
        input_data
    )[0]

    class_names = rf_model.classes_

    predicted_class_index = list(
        class_names
    ).index(prediction)

    # --------------------------------------------------------
    # Extract SHAP values safely
    # --------------------------------------------------------

    if isinstance(shap_values, list):

        values = shap_values[
            predicted_class_index
        ][0]

    else:

        shap_array = np.asarray(
            shap_values
        )

        if shap_array.ndim == 3:

            values = shap_array[
                0,
                :,
                predicted_class_index
            ]

        else:

            values = shap_array[0]

    # --------------------------------------------------------
    # Create dataframe
    # --------------------------------------------------------

    explanation_df = pd.DataFrame({

        "feature":
            feature_names,

        "shap_value":
            values,

        "absolute_importance":
            np.abs(values)

    })

    explanation_df = (
        explanation_df
        .sort_values(
            "absolute_importance",
            ascending=False
        )
    )

    # --------------------------------------------------------
    # Current input values
    # --------------------------------------------------------

    current_score_state = (
        input_data.iloc[0]["score_state"]
    )

    current_distance = (
        input_data.iloc[0]["distance_group"]
    )

    current_field_zone = (
        input_data.iloc[0]["field_zone"]
    )

    current_time_state = (
        input_data.iloc[0]["time_state"]
    )

    # --------------------------------------------------------
    # Human-readable explanations
    # --------------------------------------------------------

    explanations = []

    for _, row in explanation_df.iterrows():

        feature = row["feature"]

        shap_value = float(
            row["shap_value"]
        )

        # Ignore extremely small effects
        if abs(shap_value) < 0.005:
            continue

        # ----------------------------------------------------
        # Default display name
        # ----------------------------------------------------

        display_name = (
            FEATURE_DISPLAY_NAMES.get(
                feature,
                feature
            )
        )

        # ----------------------------------------------------
        # CATEGORICAL FEATURES
        #
        # Only show the category that is actually selected.
        # This prevents outputs such as:
        #
        # "Leading" input
        # ↓ Trailing
        #
        # ----------------------------------------------------

        if feature.startswith("categorical__"):

            # ------------------------------------------------
            # SCORE STATE
            # ------------------------------------------------

            if "score_state_TRAILING" in feature:

                if current_score_state == "TRAILING":

                    display_name = "Trailing"

                else:

                    continue

            elif "score_state_TIED" in feature:

                if current_score_state == "TIED":

                    display_name = "Game tied"

                else:

                    continue

            elif "score_state_LEADING" in feature:

                if current_score_state == "LEADING":

                    display_name = "Leading"

                else:

                    continue

            # ------------------------------------------------
            # DISTANCE GROUP
            # ------------------------------------------------

            elif "distance_group_SHORT" in feature:

                if current_distance == "SHORT":

                    display_name = "Short distance"

                else:

                    continue

            elif "distance_group_MEDIUM" in feature:

                if current_distance == "MEDIUM":

                    display_name = "Medium distance"

                else:

                    continue

            elif "distance_group_LONG" in feature:

                if current_distance == "LONG":

                    display_name = "Long distance"

                else:

                    continue

            elif "distance_group_VERY_LONG" in feature:

                if current_distance == "VERY_LONG":

                    display_name = "Very long distance"

                else:

                    continue

            # ------------------------------------------------
            # FIELD ZONE
            # ------------------------------------------------

            elif "field_zone_OWN_TERRITORY" in feature:

                if current_field_zone == "OWN_TERRITORY":

                    display_name = "Own territory"

                else:

                    continue

            elif "field_zone_MIDFIELD" in feature:

                if current_field_zone == "MIDFIELD":

                    display_name = "Field position"

                else:

                    continue

            elif "field_zone_OPPONENT_21_35" in feature:

                if current_field_zone == "OPPONENT_21_35":

                    display_name = "Opponent territory"

                else:

                    continue

            elif "field_zone_RED_ZONE" in feature:

                if current_field_zone == "RED_ZONE":

                    display_name = "Red zone"

                else:

                    continue

            # ------------------------------------------------
            # TIME STATE
            # ------------------------------------------------

            elif "time_state_EARLY" in feature:

                if current_time_state == "EARLY":

                    display_name = "Early game"

                else:

                    continue

            elif "time_state_MID" in feature:

                if current_time_state == "MID":

                    display_name = "Middle of game"

                else:

                    continue

            elif "time_state_LATE" in feature:

                if current_time_state == "LATE":

                    display_name = "Late game"

                else:

                    continue

        # ----------------------------------------------------
        # Direction
        # ----------------------------------------------------

        if shap_value > 0:

            direction = "supports"

        else:

            direction = "opposes"

        # ----------------------------------------------------
        # Add explanation
        # ----------------------------------------------------

        explanations.append({

            "feature":
                display_name,

            "direction":
                direction,

            "impact":
                round(
                    abs(shap_value),
                    4
                )

        })

        # ----------------------------------------------------
        # Only show strongest 6 meaningful factors
        # ----------------------------------------------------

        if len(explanations) >= 6:
            break

    return explanations


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_decision(
    ydstogo,
    yardline_100,
    score_differential,
    game_seconds_remaining,
    distance_group,
    field_zone,
    score_state,
    time_state
):

    # --------------------------------------------------------
    # Create input dataframe
    # --------------------------------------------------------

    input_data = pd.DataFrame([
        {

            "ydstogo":
                ydstogo,

            "yardline_100":
                yardline_100,

            "score_differential":
                score_differential,

            "game_seconds_remaining":
                game_seconds_remaining,

            "distance_group":
                distance_group,

            "field_zone":
                field_zone,

            "score_state":
                score_state,

            "time_state":
                time_state

        }
    ])

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(
        input_data
    )[0]

    # --------------------------------------------------------
    # Probabilities
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        input_data
    )[0]

    classes = model.classes_

    probability_dict = {

        class_name:
            float(probability)

        for class_name, probability
        in zip(
            classes,
            probabilities
        )

    }

    # --------------------------------------------------------
    # SHAP explanations
    # --------------------------------------------------------

    shap_explanations = (
        get_shap_explanation(
            input_data
        )
    )

    # --------------------------------------------------------
    # Human explanation
    # --------------------------------------------------------

    reasons = []

    # Distance
    if ydstogo <= 3:

        reasons.append(
            "Only a short distance is required"
        )

    elif ydstogo <= 5:

        reasons.append(
            "The distance to gain is manageable"
        )

    elif ydstogo >= 8:

        reasons.append(
            "A long distance is required"
        )

    # Score state
    if score_state == "TRAILING":

        reasons.append(
            "The team is trailing"
        )

    elif score_state == "LEADING":

        reasons.append(
            "The team is leading"
        )

    else:

        reasons.append(
            "The game is tied"
        )

    # Time state
    if time_state == "LATE":

        reasons.append(
            "The game is in a late-game situation"
        )

    elif time_state == "MID":

        reasons.append(
            "The game is in the middle stage"
        )

    else:

        reasons.append(
            "The game is in an early stage"
        )

    # Field zone
    if field_zone == "RED_ZONE":

        reasons.append(
            "The team is in the red zone"
        )

    elif field_zone == "MIDFIELD":

        reasons.append(
            "The team is around midfield"
        )

    elif field_zone == "OWN_TERRITORY":

        reasons.append(
            "The team is in its own territory"
        )

    elif field_zone == "OPPONENT_21_35":

        reasons.append(
            "The team is in opponent territory"
        )

    # --------------------------------------------------------
    # Final structured result
    # --------------------------------------------------------

    result = {

        "recommended_decision":
            prediction,

        "probabilities": {

            "PUNT":
                round(
                    probability_dict.get(
                        "PUNT",
                        0
                    ) * 100,
                    2
                ),

            "FIELD_GOAL":
                round(
                    probability_dict.get(
                        "FIELD_GOAL",
                        0
                    ) * 100,
                    2
                ),

            "GO":
                round(
                    probability_dict.get(
                        "GO",
                        0
                    ) * 100,
                    2
                )

        },

        "confidence":
            round(
                max(
                    probability_dict.values()
                ) * 100,
                2
            ),

        "human_explanation":
            reasons,

        "model_factors":
            shap_explanations

    }

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 65)
    print("FOURTHDOWNIQ — INTELLIGENT PREDICTION")
    print("=" * 65)

    # --------------------------------------------------------
    # Test situation
    # --------------------------------------------------------

    result = predict_decision(

        ydstogo=4,

        yardline_100=62,

        score_differential=-3,

        game_seconds_remaining=135,

        distance_group="SHORT",

        field_zone="MIDFIELD",

        score_state="LEADING",

        time_state="EARLY"

    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    print("\nRECOMMENDATION")
    print("-" * 30)

    print(
        f"Decision: "
        f"{result['recommended_decision']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence']}%"
    )

    # --------------------------------------------------------
    # Probabilities
    # --------------------------------------------------------

    print("\nPROBABILITIES")
    print("-" * 30)

    for decision, probability in (
        result["probabilities"].items()
    ):

        print(
            f"{decision:12} "
            f"{probability}%"
        )

    # --------------------------------------------------------
    # Human explanation
    # --------------------------------------------------------

    print("\nWHY?")
    print("-" * 30)

    for reason in (
        result["human_explanation"]
    ):

        print(
            f"- {reason}"
        )

    # --------------------------------------------------------
    # SHAP factors
    # --------------------------------------------------------

    print("\nMODEL FACTORS")
    print("-" * 30)

    for factor in (
        result["model_factors"]
    ):

        arrow = (
            "↑"
            if factor["direction"] == "supports"
            else "↓"
        )

        print(
            f"{arrow} "
            f"{factor['feature']:30} "
            f"{factor['impact']}"
        )

    print("\n")
    print("=" * 65)
    print("Prediction completed successfully!")
    print("=" * 65)