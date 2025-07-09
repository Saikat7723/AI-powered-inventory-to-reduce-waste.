import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

def train_model():
    data = pd.read_csv("data/sales_data.csv")

    X = data[["day_of_week", "is_holiday", "temperature"]]
    y = data["units_sold"]

    model = RandomForestRegressor()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train_model()

