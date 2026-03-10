import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib


def train_model():

    data = pd.read_csv("data/sample_activity_data.csv")

    X = data[["transport", "electricity"]]
    y = data["emission"]

    model = LinearRegression()

    model.fit(X, y)

    joblib.dump(model, "ai_models/carbon_prediction_model.pkl")

    print("Model trained and saved.")


if __name__ == "__main__":
    train_model()