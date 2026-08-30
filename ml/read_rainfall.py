from netCDF4 import Dataset

file_path = "data/rainfall/data.nc4"

dataset = Dataset(file_path, mode="r")

print("========== FILE INFORMATION ==========")
print(dataset)

print("\n========== VARIABLES ==========")

for variable in dataset.variables:
    print(variable)

dataset.close()