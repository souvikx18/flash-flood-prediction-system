from netCDF4 import Dataset, num2date
import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. Open NASA IMERG file
# --------------------------------------------------

file_path = "data/rainfall/data.nc4"

dataset = Dataset(file_path, mode="r")

# --------------------------------------------------
# 2. Read variables
# --------------------------------------------------

lat = dataset.variables["lat"][:]
lon = dataset.variables["lon"][:]
precipitation = dataset.variables["precipitation"][:]
time = dataset.variables["time"][:]

# --------------------------------------------------
# 3. Convert time
# --------------------------------------------------

time_variable = dataset.variables["time"]

dates = num2date(
    time,
    units=time_variable.units,
    calendar=getattr(time_variable, "calendar", "standard")
)

# --------------------------------------------------
# 4. Convert precipitation to normal NumPy array
# --------------------------------------------------

rain = np.ma.filled(precipitation, np.nan)

# --------------------------------------------------
# 5. Create rows
# --------------------------------------------------

rows = []

for t in range(rain.shape[0]):

    for i in range(len(lon)):

        for j in range(len(lat)):

            value = rain[t, i, j]

            if not np.isnan(value):

                rows.append({
                    "timestamp": str(dates[t]),
                    "latitude": float(lat[j]),
                    "longitude": float(lon[i]),
                    "rainfall_mm_hr": float(value)
                })

# --------------------------------------------------
# 6. Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(rows)

# --------------------------------------------------
# 7. Save CSV
# --------------------------------------------------

output_file = "data/rainfall/rainfall.csv"

df.to_csv(output_file, index=False)

# --------------------------------------------------
# 8. Display information
# --------------------------------------------------

print("========== RAINFALL CSV CREATED ==========")

print("Rows:", len(df))

print("\nFirst 10 rows:")
print(df.head(10))

print("\nRainfall statistics:")
print(df["rainfall_mm_hr"].describe())

print("\nSaved to:")
print(output_file)

dataset.close()