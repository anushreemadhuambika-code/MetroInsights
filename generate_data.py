import pandas as pd
import random
from datetime import datetime, timedelta

stations = ["Aluva", "Maharajas", "Edappally", "MG Road", "Vyttila"]

times = [
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00"
]

data = []

start_date = datetime(2026, 7, 1)

for day in range(30):

    current_date = start_date + timedelta(days=day)

    if current_date.weekday() >= 5:
        day_type = "Weekend"
    else:
        day_type = "Weekday"

    for station in stations:

        for time in times:

            hour = int(time[:2])

            # Base passenger demand
            if 7 <= hour <= 9:
                base_demand = 4500
            elif 17 <= hour <= 20:
                base_demand = 5000
            elif 10 <= hour <= 16:
                base_demand = 2800
            else:
                base_demand = 2000

            # Station variation
            if station == "Aluva":
                station_factor = 1.10
            elif station == "Maharajas":
                station_factor = 1.00
            elif station == "Edappally":
                station_factor = 1.15
            elif station == "MG Road":
                station_factor = 1.20
            else:
                station_factor = 1.05

            # Weekend usually has lower commuter demand
            if day_type == "Weekend":
                day_factor = 0.80
            else:
                day_factor = 1.00

            # Small random variation
            random_factor = random.uniform(0.90, 1.10)

            passengers = int(
                base_demand
                * station_factor
                * day_factor
                * random_factor
            )

            data.append([
                current_date.strftime("%Y-%m-%d"),
                time,
                station,
                day_type,
                passengers
            ])

df = pd.DataFrame(
    data,
    columns=[
        "date",
        "time",
        "station",
        "day_type",
        "passengers"
    ]
)

df.to_csv("train_data.csv", index=False)

print("Dataset created successfully!")
print("Total records:", len(df))