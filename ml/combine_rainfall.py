import os
from netCDF4 import Dataset, num2date
import pandas as pd
import numpy as np

INPUT_DIR = "data/rainfall/2024-07"
OUTPUT_FILE = "data/rainfall/rainfall_3days.csv"

all_rows = []

files = sorted([
    f for f in os.listdir(INPUT_DIR)
    if f.endswith(".nc4")
])

print(f"Found {len(files)} NetCDF files.")

for count, filename in enumerate(files, 1):

    file_path = os.path.join(INPUT_DIR, filename)

    print(f"[{count}/{len(files)}] Processing {filename}")

    try:
        dataset = Dataset(file_path, mode="r")

        lat = dataset.variables["lat"][:]
        lon = dataset.variables["lon"][:]
        precipitation = dataset.variables["precipitation"][:]
        time = dataset.variables["time"][:]

        time_variable = dataset.variables["time"]

        dates = num2date(
            time,
            units=time_variable.units,
            calendar=getattr(
                time_variable,
                "calendar",
                "standard"
            )
        )

        rain = np.ma.filled(
            precipitation,
            np.nan
        )

        for t in range(rain.shape[0]):

            for i in range(len(lon)):

                for j in range(len(lat)):

                    value = rain[t, i, j]

                    if not np.isnan(value):

                        all_rows.append({
                            "timestamp": str(dates[t]),
                            "latitude": float(lat[j]),
                            "longitude": float(lon[i]),
                            "rainfall_mm_hr": float(value)
                        })

        dataset.close()

    except Exception as e:

        print(
            f"ERROR processing {filename}: {e}"
        )

# Create DataFrame

df = pd.DataFrame(all_rows)

# Remove duplicate records

df = df.drop_duplicates()

# Sort

df = df.sort_values(
    by=[
        "timestamp",
        "latitude",
        "longitude"
    ]
)

# Save

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n==============================")
print("COMBINATION COMPLETE")
print("==============================")

print("Total rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10))

print("\nRainfall statistics:")
print(df["rainfall_mm_hr"].describe())

print("\nSaved to:")
print(OUTPUT_FILE)