import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def predict_next_year(df):
    """
    Takes the generation DataFrame and predicts the next 12 months.
    Returns a dict with predicted values and their period labels.
    """
    df = df.copy().sort_values("period")
    df["month_index"] = np.arange(len(df))

    X = df[["month_index"]].values
    y = df["generation"].values
    model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model.fit(X, y)

    # predict next year
    last_index = int(df["month_index"].iloc[-1])
    future_indices = np.arange(last_index + 1, last_index + 13).reshape(-1, 1)
    predictions = model.predict(future_indices)

    # taking out the negative values
    predictions = [max(0, round(p, 2)) for p in predictions]

    # to create dates
    last_period = df["period"].iloc[-1]
    last_year, last_month = map(int, last_period.split("-"))
    future_labels = []
    for i in range(12):
        month = (last_month + i) % 12 + 1
        year  = last_year + (last_month + i) // 12
        future_labels.append(f"{year}-{month:02d}")

    return {
        "labels": future_labels,
        "values": predictions
    }