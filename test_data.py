import nflreadpy as nfl
import polars as pl

print("Loading NFL data...")

# ==========================================
# 1. LOAD NFL DATA
# ==========================================

pbp = nfl.load_pbp(seasons=[2025])

print("Data loaded!")

# ==========================================
# 2. KEEP ONLY FOURTH-DOWN PLAYS
# ==========================================

fourth_downs = pbp.filter(
    pl.col("down") == 4
)

print("Fourth-down plays:", fourth_downs.shape[0])

# ==========================================
# 3. REMOVE INVALID / NON-DECISION PLAYS
# ==========================================

fourth_downs = fourth_downs.filter(
    ~pl.col("play_type").is_in([
        "no_play",
        "qb_kneel"
    ])
)

print("After cleaning:", fourth_downs.shape[0])

# ==========================================
# 4. CLASSIFY THE COACH'S DECISION
# ==========================================

fourth_downs = fourth_downs.with_columns(
    pl.when(pl.col("play_type") == "field_goal")
      .then(pl.lit("FIELD_GOAL"))

      .when(pl.col("play_type") == "punt")
      .then(pl.lit("PUNT"))

      .when(pl.col("play_type").is_in(["pass", "run"]))
      .then(pl.lit("GO"))

      .otherwise(pl.lit("OTHER"))

      .alias("decision")
)

# Remove anything classified as OTHER
fourth_downs = fourth_downs.filter(
    pl.col("decision") != "OTHER"
)

print("Final ML decisions:", fourth_downs.shape[0])

# ==========================================
# 5. CREATE DISTANCE GROUP
# ==========================================

fourth_downs = fourth_downs.with_columns(
    pl.when(pl.col("ydstogo") <= 2)
      .then(pl.lit("SHORT"))

      .when(pl.col("ydstogo") <= 5)
      .then(pl.lit("MEDIUM"))

      .when(pl.col("ydstogo") <= 10)
      .then(pl.lit("LONG"))

      .otherwise(pl.lit("VERY_LONG"))

      .alias("distance_group")
)

# ==========================================
# 6. CREATE FIELD POSITION ZONE
# ==========================================

fourth_downs = fourth_downs.with_columns(
    pl.when(pl.col("yardline_100") <= 20)
      .then(pl.lit("RED_ZONE"))

      .when(pl.col("yardline_100") <= 35)
      .then(pl.lit("OPPONENT_21_35"))

      .when(pl.col("yardline_100") <= 50)
      .then(pl.lit("MIDFIELD"))

      .otherwise(pl.lit("OWN_TERRITORY"))

      .alias("field_zone")
)

# ==========================================
# 7. CREATE SCORE SITUATION
# ==========================================

fourth_downs = fourth_downs.with_columns(
    pl.when(pl.col("score_differential") > 0)
      .then(pl.lit("LEADING"))

      .when(pl.col("score_differential") < 0)
      .then(pl.lit("TRAILING"))

      .otherwise(pl.lit("TIED"))

      .alias("score_state")
)

# ==========================================
# 8. CREATE TIME SITUATION
# ==========================================

fourth_downs = fourth_downs.with_columns(
    pl.when(pl.col("game_seconds_remaining") <= 300)
      .then(pl.lit("LATE"))

      .when(pl.col("game_seconds_remaining") <= 1800)
      .then(pl.lit("MID"))

      .otherwise(pl.lit("EARLY"))

      .alias("time_state")
)

# ==========================================
# 9. SELECT ML FEATURES
# ==========================================

ml_data = fourth_downs.select([

    # Numerical features
    "ydstogo",
    "yardline_100",
    "score_differential",
    "game_seconds_remaining",

    # Categorical features
    "distance_group",
    "field_zone",
    "score_state",
    "time_state",

    # Target
    "decision"
])

# ==========================================
# 10. REMOVE MISSING VALUES
# ==========================================

ml_data = ml_data.drop_nulls()

print("ML dataset shape:", ml_data.shape)

# ==========================================
# 11. SHOW SAMPLE
# ==========================================

print("\nSample ML dataset:")
print(ml_data.head(15))

# ==========================================
# 12. SHOW TARGET DISTRIBUTION
# ==========================================

print("\nDecision distribution:")

print(
    ml_data
    .group_by("decision")
    .agg(
        pl.len().alias("plays")
    )
    .sort("plays", descending=True)
)

# ==========================================
# 13. SAVE ML DATASET
# ==========================================

ml_data.write_csv("fourth_down_ml.csv")

print("\n==========================================")
print("SUCCESS!")
print("Saved: fourth_down_ml.csv")
print("==========================================")

# ==========================================
# SAVE ML DATASET
# ==========================================

ml_data = fourth_downs.select([
    # Situation features
    "ydstogo",
    "yardline_100",
    "score_differential",
    "game_seconds_remaining",

    # Categorized situation features
    "distance_group",
    "field_zone",
    "score_state",
    "time_state",

    # Target
    "decision",

    # Outcome metrics
    "epa",
    "wpa"
])

# Remove rows with missing important values
ml_data = ml_data.drop_nulls()

# Save as CSV
ml_data.write_csv("fourth_down_ml.csv")

print("\nML dataset created!")
print("Rows:", ml_data.shape[0])
print("Columns:", ml_data.shape[1])

print("\nML dataset preview:")
print(ml_data.head(10))