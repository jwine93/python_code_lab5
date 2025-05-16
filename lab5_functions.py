#####################
# Block 1:  Import the packages you'll need
# 
# 

import os, sys
import rasterio
import geopandas as gpd
import numpy as np
from rasterstats import zonal_stats



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


import geopandas as gpd
from rasterstats import zonal_stats
import os

class SmartVector:
    def __init__(self, vector_path):
        """
        Initialize the SmartVector class with a vector file path.
        """
        self.vector_path = vector_path
        self.gdf = None  # Initialize the GeoDataFrame attribute

        # Load the vector file
        try:
            self.gdf = gpd.read_file(self.vector_path)
            print(f"Loaded vector file: {self.vector_path}")
        except Exception as e:
            raise ValueError(f"Error loading vector file: {e}")
        
        
    def summarize_field(self, field):
        """Calculate the mean value of a specified field"""
        # Set up a tracking variable to track if things work
        okay = True
        
        # Check if the field is in the dataset
        try:
            if field not in self.gdf.columns:
                okay = False
                print(f"The field {field} is not in list of possible fields")
                return False, None
        except Exception as e:
            print(f"Problem checking the fields: {e}")
            okay = False
            return False, None
        
        # Calculate the mean value
        try:
            # Filter out None and NaN values
            valid_values = self.gdf[field].dropna()
            mean = valid_values.mean()
            return okay, mean
        except Exception as e:
            print(f"Problem calculating mean: {e}")
            okay = False
            return False, None
        

    def zonal_stats_to_field(self, raster_path, statistic_type="mean", output_field="zonal_stat"):
        """
        For each feature in the vector layer, calculates the zonal statistic from the raster
        and writes it to a new field.

        Parameters:
        - raster_path: Path to the raster file.
        - statistic_type: Type of statistic to calculate (e.g., 'mean', 'sum', 'min', 'max').
        - output_field: Name of the column to store the results.

        Returns:
        - Updated GeoDataFrame with the new column.
        """
        # Set up a tracking variable to track if things work
        okay = True

        # Check if the raster file exists
        if not os.path.exists(raster_path):
            print(f"Raster file not found: {raster_path}")
            return False

        # Add a field to store the zonal stats result
        if output_field in self.gdf.columns:
            print(f"Field '{output_field}' already exists. Will overwrite values.")
        else:
            print(f"Adding field '{output_field}' to store zonal statistics.")

        # Calculate zonal statistics
        try:
            print("Starting zonal statistics calculation...")
            stats = zonal_stats(self.gdf, raster_path, stats=statistic_type, geojson_out=False)
            print(f"Calculated zonal statistics for {raster_path}")
        except Exception as e:
            print(f"Error calculating zonal statistics: {e}")
            return False

        # Add the statistics to the GeoDataFrame
        try:
            self.gdf[output_field] = [s[statistic_type] for s in stats]
            print(f"Zonal statistics '{statistic_type}' added to field '{output_field}'.")
        except Exception as e:
            print(f"Error adding zonal statistics to GeoDataFrame: {e}")
            okay = False
            return okay

        return okay

    def save_as(self, output_path):
        """
        Save the updated GeoDataFrame to a new file.

        Parameters:
        - output_path: Path to save the updated vector file.
        """
        try:
            self.gdf.to_file(output_path)
            print(f"Saved updated vector file to {output_path}.")
        except Exception as e:
            raise ValueError(f"Error saving vector file: {e}")