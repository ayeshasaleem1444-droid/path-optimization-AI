import random

import pandas as pd

random.seed(42)

rows = []
for i in range(600):
    distance_km = round(random.uniform(2, 25), 2)
    speed_kmh = random.uniform(28, 40)
    osrm_duration = round(distance_km / speed_kmh * 60, 1)
    hour = random.randint(0, 23)
    vehicle = random.choice(["car", "bike", "rickshaw"])
    is_peak = 1 if (7 <= hour <= 9) or (17 <= hour <= 20) else 0

    if vehicle == "car":
        multiplier = random.uniform(1.4, 1.9) if is_peak else random.uniform(1.05, 1.25)
    elif vehicle == "bike":
        multiplier = random.uniform(1.15, 1.4) if is_peak else random.uniform(1.0, 1.15)
    else:
        multiplier = random.uniform(1.3, 1.6) if is_peak else random.uniform(1.15, 1.35)

    actual_duration = round(osrm_duration * multiplier, 1)
    rows.append([distance_km, osrm_duration, hour, is_peak, vehicle, actual_duration])


df = pd.DataFrame(
    rows,
    columns=[
        "distance_km",
        "osrm_duration_min",
        "hour",
        "is_peak",
        "vehicle",
        "actual_duration_min",
    ],
)

print(df.head())
df.to_csv("lahore_trips.csv", index=False)
print("Saved", len(df), "rows")

df["ratio"] = df["actual_duration_min"] / df["osrm_duration_min"]

print(df.groupby(["is_peak", "vehicle"])["ratio"].mean())
