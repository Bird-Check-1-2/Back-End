from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

import category_encoders as ce
import pandas as pd
import numpy as np

# ======================================

print("Reading in labeled dataset sample...")
print()

df = pd.read_csv("sample/labelled_bird_sample.csv")
print("Rows in dataset:", df.shape[0])
# assert(df.shape == (103992, 16))

# ========================================

print("Select features and target to split dataframe into X and y...")
print()

features = ['name', 'season', 'region']
target = 'target'

X = df[features]
y = df[target]

print("Feature columns:", X.shape[1])
# assert(X.shape == (103992, 3))
# assert(y.shape == (103992,))

# Saving list of birds, seasons, and regions
birds_list = X['name'].unique().tolist()
seasons_list = X['season'].unique().tolist()
regions_list = X['region'].unique().tolist()

dump(birds_list, 'utils/birds_list.p')
dump(seasons_list, 'utils/seasons_list.p')

# =======================================

print("Encoding categorical features...")
print()

encoder = ce.CatBoostEncoder()

X = encoder.fit_transform(X, y)

# ======================================

print("Splitting X and y into train and test...")
print()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Observations in train set:", X_train.shape[0])
print("Observations in test set:", X_test.shape[0])

# assert(X_train.shape == (83193, 3))
# assert(X_test.shape == (20799, 3))
# assert(y_train.shape == (83193,))
# assert(y_test.shape == (20799,))

# =====================================

print("Training Random Forest Classifier...")
print()

model = RandomForestClassifier(n_estimators=500, max_depth=12, random_state=42)
model.fit(X_train, y_train)

# =====================================

print("Making predictions and fetching score...")
print()

preds = model.predict(X_test)

print("\n\n")
print("ACCURACY SCORE: ")
print("================")
print(f"    {accuracy_score(y_test, preds)}    ")
print("================")
print("\n\n")
# =======================================

print("Saving encoder and model... ")
print()

dump(model, "utils/rf.p")
dump(encoder, "utils/cat_boost.p")
