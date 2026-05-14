import pandas as pd
from model import predict_next_year

def make_charts(df, state, metric):
    df = df.copy()
    df["generation"] = pd.to_numeric(df["generation"], errors="coerce")
    df = df.dropna(subset=["generation"])
    df = df.sort_values("period")

    # this is a line chart
    line_labels = df["period"].tolist()
    line_values = df["generation"].round(2).tolist()

    # these are the predictions
    predictions = predict_next_year(df)
    pred_labels = predictions["labels"]
    pred_values = predictions["values"]

    # this is a bar chart
    df["year"] = df["period"].str[:4]
    yearly = df.groupby("year")["generation"].mean().round(2)
    bar_labels = yearly.index.tolist()
    bar_values = yearly.values.tolist()

    # this is a histogram
    values = df["generation"].tolist()
    min_val = min(values)
    max_val = max(values)
    bin_count = 8
    bin_size = (max_val - min_val) / bin_count if max_val != min_val else 1

    # calculating the buckets
    bins = [0] * bin_count
    bin_labels = []
    for i in range(bin_count):
        low  = round(min_val + i * bin_size, 1)
        high = round(min_val + (i + 1) * bin_size, 1)
        bin_labels.append(f"{low}–{high}")

    for v in values:
        idx = int((v - min_val) / bin_size)
        if idx >= bin_count:
            idx = bin_count - 1
        bins[idx] += 1

    return {
        "line": {
            "labels": line_labels,
            "values": line_values,
            "pred_labels": pred_labels,
            "pred_values": pred_values
        },
        "bar":       {"labels": bar_labels,  "values": bar_values},
        "histogram": {"labels": bin_labels,   "values": bins},
    }