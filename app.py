from flask import Flask, request, render_template
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    from eia_api import fetch_data
    from analysis import get_stats
    from charts import make_charts
    from model import predict_next_year

    state      = request.form["state"]
    metric     = request.form["metric"]
    start_year = request.form["start_year"]
    end_year   = request.form["end_year"]

    try:
        df = fetch_data(state, metric, start_year, end_year)
    except ValueError as e:
        metric_names = {
            "SUN": "Solar", "WND": "Wind", "NG": "Natural Gas",
            "COL": "Coal",  "NUC": "Nuclear"
        }
        return render_template(
            "no_data.html",
            state=state,
            metric=metric_names.get(metric, metric),
            reason=str(e)
        ), 200

    df.to_csv(f"data/{state}_{metric}.csv", index=False)

    stats      = get_stats(df)
    chart_data = make_charts(df, state, metric)
    predictions = predict_next_year(df)

    metric_names = {
        "SUN": "Solar", "WND": "Wind", "NG": "Natural Gas",
        "COL": "Coal",  "NUC": "Nuclear"
    }
    metric_label = metric_names.get(metric, metric)

    return render_template(
        "dashboard.html",
        state=state,
        metric=metric_label,
        stats=stats,
        chart_data=json.dumps(chart_data),
        pred_next_avg=round(sum(predictions["values"]) / 12, 2),
        pred_labels=predictions["labels"]
    )

if __name__ == "__main__":
    app.run(debug=True)