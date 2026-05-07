import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")

def fetch_data(state, metric, start_year, end_year):
    url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data"

    my_params = {
        "api_key": API_KEY,
        "frequency": "monthly",
        "data[]": "generation",
        "facets[location][]": state,
        "facets[fueltypeid][]": metric,
        "facets[sectorid][]": "2",
        "start": f"{start_year}-01",
        "end": f"{end_year}-12",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": 500,
    }

    response = requests.get(url, params=my_params)
    json_data = response.json()

    if "response" not in json_data:
        raise ValueError(f"Unexpected API response: {json_data}")

    records = json_data["response"].get("data", [])

    if not records:
        raise ValueError(f"No data returned for state={state}, metric={metric}. "
                         f"The EIA may not have data for this combination.")

    df = pd.DataFrame(records)

    if "generation" not in df.columns:
        raise KeyError(f"'generation' column not found. Available columns: {df.columns.tolist()}")

    df["generation"] = pd.to_numeric(df["generation"], errors="coerce")
    df = df.dropna(subset=["generation"])

    return df