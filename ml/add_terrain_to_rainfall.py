import pandas as pd
import rasterio
import numpy as np

# ---------------------------------------
# Files
# ---------------------------------------

RAINFALL_FILE = "data/rainfall/rainfall_3days.csv"

ELEVATION_FILE = "data/dem/elevation.tif"

SLOPE_FILE = "data/dem/slope.tif"

OUTPUT_FILE = "data/rainfall/rainfall_terrain.csv"


# ---------------------------------------
# Load rainfall CSV
# ---------------------------------------

print("Loading rainfall data...")

df = pd.read_csv(RAINFALL_FILE)

print("Rainfall rows:", len(df))


# ---------------------------------------
# Open elevation and slope
# ---------------------------------------

with rasterio.open(ELEVATION_FILE) as elevation_src, \
     rasterio.open(SLOPE_FILE) as slope_src:

    print("Elevation CRS:", elevation_src.crs)
    print("Slope CRS:", slope_src.crs)

    # Coordinates from rainfall dataset
    coordinates = list(
        zip(
            df["longitude"],
            df["latitude"]
        )
    )

    # Extract elevation
    elevation_values = []

    for value in elevation_src.sample(coordinates):

        elevation_values.append(
            float(value[0])
        )

    # Extract slope
    slope_values = []

    for value in slope_src.sample(coordinates):

        slope_values.append(
            float(value[0])
        )


# ---------------------------------------
# Add features
# ---------------------------------------

df["elevation_m"] = elevation_values

df["slope_degree"] = slope_values


# ---------------------------------------
# Handle NoData
# ---------------------------------------

df["elevation_m"] = df["elevation_m"].replace(
    -9999,
    np.nan
)

df["slope_degree"] = df["slope_degree"].replace(
    -9999,
    np.nan
)


# ---------------------------------------
# Remove rows with missing terrain
# ---------------------------------------

before = len(df)

df = df.dropna(
    subset=[
        "elevation_m",
        "slope_degree"
    ]
)

after = len(df)

print("\nRows before terrain filtering:", before)
print("Rows after terrain filtering:", after)


# ---------------------------------------
# Save
# ---------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------
# Results
# ---------------------------------------

print("\n========== SUCCESS ==========")

print(
    "Saved:",
    OUTPUT_FILE
)

print("\nColumns:")

print(
    df.columns.tolist()
)

print("\nFirst 5 rows:")

print(
    df.head()
)

print("\nElevation statistics:")

print(
    df["elevation_m"].describe()
)

print("\nSlope statistics:")

print(
    df["slope_degree"].describe()
)