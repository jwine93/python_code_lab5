# Lab 5 scripts

import lab5_functions as l5

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
finally:
    # Close the raster file
    landsat_raster.close()


# Part 2:
# Assign a variable to the parcels data shapefile path


#  Pass this to your new smart vector class


#  Calculate zonal statistics and add to the attribute table of the parcels shapefile



#  Part 3: Optional
#  Use matplotlib to make a map of your census tracts with the average NDVI values









