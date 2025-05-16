#####################
# Block 1:  Import the packages you'll need
# 
# 

import os, sys
import rasterio
import geopandas as gpd
import numpy as np



##################
# Block 2: 
# set the working directory to the directory where the data are

# Change this to the directory where your data are

data_dir = r"R:/2025/Spring/GEOG562/Students/wineju/Lab5_2025"
os.chdir(data_dir)
print(os.getcwd())


##################
# Block 3: 
#   Set up a new smart raster class using rasterio  
#    that will have a method called "calculate_ndvi"


class SmartRaster:
    def __init__(self, raster_path):
        """
        Initialize the SmartRaster class with a raster file path.
        """
        self.raster_path = raster_path
        try:
            self.dataset = rasterio.open(raster_path)
        except Exception as e:
            raise ValueError(f"Error opening raster file: {e}")

    def calculate_ndvi(self, red_band_index=3, nir_band_index=4):
        """
        Calculate the NDVI (Normalized Difference Vegetation Index).
        
        Parameters:
        - red_band_index: Index of the red band (default is 3).
        - nir_band_index: Index of the NIR band (default is 4).
        
        Returns:
        - NDVI as a NumPy array.
        """
        try:
            with rasterio.open(self.raster_path) as dataset:
                # Read the red and NIR bands
                red = dataset.read(red_band_index).astype('float32')
                nir = dataset.read(nir_band_index).astype('float32')
                
                # Avoid division by zero
                np.seterr(divide='ignore', invalid='ignore')
                
                # Calculate NDVI
                ndvi = (nir - red) / (nir + red)
                
                # Handle NaN values
                ndvi = np.nan_to_num(ndvi, nan=-1.0)
                
                return ndvi
        except Exception as e:
            raise ValueError(f"Error calculating NDVI: {e}")
        
    def save_ndvi(self, output_path, ndvi, dtype="float32"):
        """
        Save the calculated NDVI to an output file.
    
        Parameters:
        - output_path: Path to the output file.
        - ndvi: The NDVI array to save.
        - dtype: Data type for the output file (default is 'float32').
        """
        try:
            # Copy metadata from the input raster
            meta = self.dataset.meta.copy()
            meta.update({
                "dtype": dtype,  # Set the data type
                "count": 1,      # Single band for NDVI
                "driver": "GTiff"  # Output format
            })
    
            # Write the NDVI array to the output file
            with rasterio.open(output_path, "w", **meta) as dst:
                dst.write(ndvi, 1)  # Write NDVI to the first band
        except Exception as e:
            raise ValueError(f"Error saving NDVI: {e}")


    def close(self):
        """
        Close the raster dataset.
        """
        self.dataset.close()






##################
# Block 4: 
#   Set up a new smart vector class using geopandas
#    that will have a method similar to what did in lab 4
#    to calculate the zonal statistics for a raster
#    and add them as a column to the attribute table of the vector

