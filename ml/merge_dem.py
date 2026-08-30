import glob
import rasterio
from rasterio.merge import merge

files = glob.glob("data/dem/*.tif")

# Ignore the duplicate if it still exists
files = [f for f in files if " 2.tif" not in f]

print(f"Found {len(files)} DEM tiles")

src_files = [rasterio.open(f) for f in files]

mosaic, transform = merge(src_files)

profile = src_files[0].profile.copy()
profile.update(
    height=mosaic.shape[1],
    width=mosaic.shape[2],
    transform=transform
)

output = "data/dem/merged_dem.tif"

with rasterio.open(output, "w", **profile) as dst:
    dst.write(mosaic)

for src in src_files:
    src.close()

print("========== SUCCESS ==========")
print(f"Merged DEM saved to: {output}")
print(f"DEM shape: {mosaic.shape}")