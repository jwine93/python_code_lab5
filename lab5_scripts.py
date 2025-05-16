# Lab 5 scripts

import lab5_functions as l5
import importlib

#  Part 1:

#  Assign a variable to the Landsat file 

landsat_file = r"R:\2025\Spring\GEOG562\Students\wineju\Lab5_2025\Landsat_image_corv.tif"

# Pass this to your new smart raster class

landsat_raster = l5.SmartRaster(landsat_file)

# Calculate NDVI and save to and output file
try:
    # Calculate NDVI
    ndvi = landsat_raster.calculate_ndvi()
    print("NDVI calculated successfully.")
    # Save the NDVI to a new file
    output_file = r"R:\2025\Spring\GEOG562\Students\wineju\Lab5_2025\outputs\ndvi_output.tif"
    landsat_raster.save_ndvi(output_file, ndvi)
    print("NDVI file saved successfully.")
finally:
    # Close the raster file
    landsat_raster.close()


# Part 2:
# Assign a variable to the parcels data shapefile path
importlib.reload(l5)

parcels_file = r"R:\2025\Spring\GEOG562\Students\wineju\Lab5_2025\Benton_County_TaxLots.shp"

#  Pass this to your new smart vector class


#  Calculate zonal statistics and add to the attribute table of the parcels shapefile

output_file = r"R:\2025\Spring\GEOG562\Students\wineju\Lab5_2025\outputs\updated_parcels.shp"

# Create a SmartVector instance
vector = l5.SmartVector(parcels_file)

# Calculate zonal statistics and add them to the attribute table
if vector.zonal_stats_to_field(landsat_file, statistic_type="mean", output_field="mean_ndvi"):
    # Save the updated vector file
    vector.save_as(output_file)

#  Part 3: Optional
#  Use matplotlib to make a map of your census tracts with the average NDVI values









