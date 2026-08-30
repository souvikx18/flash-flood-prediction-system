from netCDF4 import Dataset
import pandas as pd
import numpy as np

# NASA rainfall file
file_path = "data/rainfall/data.nc4"

# Open NetCDF file
dataset = Dataset(file_path, mode="r")

print("========== VARIABLES ==========")

for name in dataset.variables:
    print(name)

# Read variables
lat = dataset.variables["lat"][:]
lon = dataset.variables["lon"][:]
precipitation = dataset.variables["precipitation"][:]

print("\n========== DATA INFORMATION ==========")

print("Latitude shape:", lat.shape)
print("Longitude shape:", lon.shape)
print("Precipitation shape:", precipitation.shape)

print("\nLatitude range:")
print(float(np.min(lat)), "to", float(np.max(lat)))

print("\nLongitude range:")
print(float(np.min(lon)), "to", float(np.max(lon)))

print("\nPrecipitation statistics:")

# Remove missing values
rain = np.ma.filled(precipitation, np.nan)

print("Minimum:", np.nanmin(rain))
print("Maximum:", np.nanmax(rain))
print("Mean:", np.nanmean(rain))

dataset.close()

print("\n========== SUCCESS ==========")
print("Rainfall data extracted successfully!")