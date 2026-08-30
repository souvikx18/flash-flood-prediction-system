import rasterio
import numpy as np
from rasterio.transform import xy

INPUT = "data/dem/merged_dem.tif"

ELEVATION_OUTPUT = "data/dem/elevation.tif"
SLOPE_OUTPUT = "data/dem/slope.tif"

with rasterio.open(INPUT) as src:

    elevation = src.read(1).astype("float32")

    # Convert SRTM NoData value to NaN
    nodata = src.nodata

    if nodata is not None:
        elevation[elevation == nodata] = np.nan

    print("========== DEM INFORMATION ==========")
    print("CRS:", src.crs)
    print("Resolution:", src.res)

    print("\nElevation:")
    print("Minimum:", np.nanmin(elevation))
    print("Maximum:", np.nanmax(elevation))
    print("Mean:", np.nanmean(elevation))

    # ------------------------------------------
    # Calculate slope
    # ------------------------------------------

    # Pixel size in degrees
    xres = src.res[0]
    yres = src.res[1]

    # Approximate conversion from degrees to metres
    # around the Himalayan region
    lat_mean = (src.bounds.top + src.bounds.bottom) / 2

    meters_per_degree_lat = 111320
    meters_per_degree_lon = (
        111320 * np.cos(np.radians(lat_mean))
    )

    xres_m = xres * meters_per_degree_lon
    yres_m = yres * meters_per_degree_lat

    # Gradient
    grad_y, grad_x = np.gradient(
        elevation,
        yres_m,
        xres_m
    )

    # Slope in degrees
    slope = np.degrees(
        np.arctan(
            np.sqrt(
                grad_x ** 2 +
                grad_y ** 2
            )
        )
    )

    slope = slope.astype("float32")

    # ------------------------------------------
    # Save elevation
    # ------------------------------------------

    profile = src.profile.copy()

    profile.update(
        dtype="float32",
        count=1,
        compress="lzw",
        nodata=-9999
    )

    elevation_save = np.where(
        np.isnan(elevation),
        -9999,
        elevation
    )

    with rasterio.open(
        ELEVATION_OUTPUT,
        "w",
        **profile
    ) as dst:

        dst.write(elevation_save, 1)

    # ------------------------------------------
    # Save slope
    # ------------------------------------------

    slope_save = np.where(
        np.isnan(slope),
        -9999,
        slope
    )

    with rasterio.open(
        SLOPE_OUTPUT,
        "w",
        **profile
    ) as dst:

        dst.write(slope_save, 1)

print("\n========== SUCCESS ==========")

print(
    "Elevation saved to:",
    ELEVATION_OUTPUT
)

print(
    "Slope saved to:",
    SLOPE_OUTPUT
)

valid_slope = slope[slope != -9999]

print("\nSlope statistics:")
print("Minimum:", np.nanmin(valid_slope))
print("Maximum:", np.nanmax(valid_slope))
print("Mean:", np.nanmean(valid_slope))