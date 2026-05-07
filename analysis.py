import pandas as pd
import numpy as np

def get_stats(df):
    generation = df["generation"].dropna()

    average = round(generation.mean(), 2)

    # max, min, total generation and when it happeneed
    max_val = round(generation.max(), 2)
    max_idx = generation.idxmax()
    max_period = df.loc[max_idx, "period"] if max_idx in df.index else "N/A"

    min_val = round(generation.min(), 2)

    total = round(generation.sum(), 2)

    # for trend I used numpy to get the slope:
    # positive slope = going up, negative = going down
    x = np.arange(len(generation))
    if len(x) > 1:
        slope, _ = np.polyfit(x, generation.values, 1)
        if slope > 0.5:
            trend = "increasing"
        elif slope < -0.5:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "N/A"

    
    # generating sentences for easier understanding
    if average > 3000:
        summary = f"This state generates a lot of this energy — about {average} thousand MWh per month on average. It's one of the bigger producers in the country."
    elif average > 1000:
        summary = f"This state generates a decent amount of this energy — about {average} thousand MWh per month on average. It makes a real contribution to the local power grid."
    elif average > 200:
        summary = f"This state generates a moderate amount of this energy — about {average} thousand MWh per month on average. It's not the main source of power here, but it plays a role."
    else:
        summary = f"This state doesn't generate much of this energy — only about {average} thousand MWh per month on average. It's a small part of how the state gets its power."

    if trend == "increasing":
        summary += " Production has been going up lately, which is a good sign for this energy source."
    elif trend == "decreasing":
        summary += " Production has been going down lately, which could mean less investment or a shift to other energy sources."

    return {
        "average": average,
        "max": max_val,
        "max_period": max_period,
        "min": min_val,
        "total": total,
        "trend": trend,
        "num_months": len(generation),
        "summary": summary,
    }