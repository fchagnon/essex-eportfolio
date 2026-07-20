import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# 1. Load Data
df = pd.read_csv('all_teams.csv')

# 2. Data Engineering: Normalize and Aggregate
# Resolving the 'AWAY'/'HOME' case-sensitivity found in the diagnostic
df['home_or_away'] = df['home_or_away'].astype(str).str.lower()

# Squash player rows into one team row per game
team_df = df.groupby(['gameId', 'team', 'home_or_away', 'gameDate']).agg({
    'xGoalsFor': 'sum',
    'xGoalsAgainst': 'sum',
    'goalsFor': 'sum',
    'goalsAgainst': 'sum',
    'corsiPercentage': 'mean',
    'xGoalsPercentage': 'mean'
}).reset_index()

# 3. Feature Engineering: Rolling Averages (The 'Prior Form' Logic)
team_df = team_df.sort_values(['team', 'gameDate'])
features_to_roll = ['xGoalsPercentage', 'corsiPercentage', 'goalsFor', 'goalsAgainst']

for feat in features_to_roll:
    # shift(1) ensures we don't 'leak' the current game's result into the predictor
    team_df[f'prev_{feat}'] = team_df.groupby('team')[feat].transform(lambda x: x.shift(1).rolling(5).mean())

team_df = team_df.dropna()

# 4. The Comparative Merge (The 'Matchup' Logic)
home_df = team_df[team_df['home_or_away'] == 'home'].copy()
away_df = team_df[team_df['home_or_away'] == 'away'].copy()

home_df['gameId'] = home_df['gameId'].astype(str)
away_df['gameId'] = away_df['gameId'].astype(str)

merged = pd.merge(home_df, away_df, on='gameId', suffixes=('_home', '_away'))

# 5. Delta & Tiebreaker Calculation
# We calculate the 'Skill Gap' and add a 'Home Constant' for the tiebreaker
for feat in features_to_roll:
    merged[f'{feat}_delta'] = merged[f'prev_{feat}_home'] - merged[f'prev_{feat}_away']

# This 'home_ice_constant' represents the baseline advantage when skill deltas are zero
merged['home_ice_constant'] = 1 

# 6. Model Training
delta_features = [f'{feat}_delta' for feat in features_to_roll] + ['home_ice_constant']
X = merged[delta_features]
y = (merged['goalsFor_home'] > merged['goalsAgainst_home']).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest effectively acts as the 'Judge' between Skill and Venue
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train_scaled, y_train)

# 7. Results Output
preds = model.predict(X_test_scaled)
print(f"Matchups analyzed: {len(merged)}")
print(f"Final Accuracy: {accuracy_score(y_test, preds):.2%}")
print("\nClassification Report:\n", classification_report(y_test, preds))

# Show which features the AI prioritized
importances = pd.Series(model.feature_importances_, index=delta_features)
print("\nPredictive Weighting (Skill vs. Venue):")
print(importances.sort_values(ascending=False))
