import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# 1. Load Data
df = pd.read_csv('all_teams.csv')
df = df.sort_values(['team', 'gameDate']) # Crucial for chronological rolling stats

# 2. Create the Target Variable ('won')
# A team wins if they score more than the opponent
df['won'] = (df['goalsFor'] > df['goalsAgainst']).astype(int)

# 3. Feature Engineering: Rolling Averages (The 'Predictive' Step)
# We use the average of the PREVIOUS 5 games to predict the CURRENT game.
features_to_roll = ['xGoalsPercentage', 'corsiPercentage', 'iceTime', 'goalsFor', 'goalsAgainst']
predictive_features = []

for feature in features_to_roll:
    new_col = f'prev_avg_{feature}'
    # shift(1) ensures we don't include the current game's result in the average
    df[new_col] = df.groupby('team')[feature].transform(lambda x: x.shift(1).rolling(5).mean())
    predictive_features.append(new_col)

# Drop rows where we don't have 5 games of history yet
df_clean = df.dropna(subset=predictive_features)

# 4. Modeling
X = df_clean[predictive_features]
y = df_clean['won']

# Maintain time order for a realistic test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train_scaled, y_train)

# 5. Output
preds = model.predict(X_test_scaled)
print(f"Predictive Accuracy: {accuracy_score(y_test, preds):.2%}")
print(classification_report(y_test, preds))
