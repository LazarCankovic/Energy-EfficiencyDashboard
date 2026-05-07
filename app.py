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

    state = request.form["state"]
    metric = request.form["metric"]
    start_year = request.form["start_year"]
    end_year = request.form["end_year"]

    try:
        df = fetch_data(state, metric, start_year, end_year)
    except ValueError as e:
        metric_names = {
            "SUN": "Solar", "WND": "Wind", "NG": "Natural Gas",
            "COL": "Coal", "NUC": "Nuclear"
        }
        return render_template(
            "no_data.html",
            state=state,
            metric=metric_names.get(metric, metric),
            reason=str(e)
        ), 200

    df.to_csv(f"data/{state}_{metric}.csv", index=False)
    stats = get_stats(df)
    chart_data = make_charts(df, state, metric)

    metric_names = {
        "SUN": "Solar", "WND": "Wind", "NG": "Natural Gas",
        "COL": "Coal", "NUC": "Nuclear"
    }

    return render_template(
        "dashboard.html",
        state=state,
        metric=metric_names.get(metric, metric),
        stats=stats,
        chart_data=json.dumps(chart_data)
    )

if __name__ == "__main__":
    app.run(debug=True)