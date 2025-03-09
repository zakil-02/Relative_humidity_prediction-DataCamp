import pandas as pd
import numpy as np
import netCDF4 as nc
import os
from tqdm import tqdm
from shapely.geometry import Point
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def prepare_climate_data(file_path, output_dir='./data'):
    """
    Process NetCDF climate data and save to CSV files with progress tracking.
    
    Args:
        file_path (str): Path to the NetCDF file
        output_dir (str): Directory to save output files
    """
    try:
        # Create output directories if they don't exist
        os.makedirs(f"{output_dir}/public", exist_ok=True)
        
        logger.info(f"Opening NetCDF file: {file_path}")
        dataset = nc.Dataset(file_path)
        
        # Extract dimensions
        valid_time = dataset.variables['valid_time'][:]
        pressure_level = dataset.variables['pressure_level'][:]
        latitude = dataset.variables['latitude'][:]
        longitude = dataset.variables['longitude'][:]
        
        # Get total number of data points for progress bar
        total_points = len(valid_time) * len(pressure_level) * len(latitude) * len(longitude)
        
        logger.info(f"Extracting variables from NetCDF file")
        # Create a dictionary of variables
        variables = {
                        'valid_time': valid_time,  # Time steps (968,)
                        'pressure_level': pressure_level,  # Pressure levels (1,)
                        'latitude': latitude,  # Latitude coordinates (59,)
                        'longitude': longitude,  # Longitude coordinates (21,)
                        'expver': dataset.variables['expver'][:],  # Experiment version (968,)
                        'divergence': dataset.variables['d'][:],  # Divergence (968, 1, 59, 21)
                        'cloud_cover': dataset.variables['cc'][:],  # Cloud cover fraction (968, 1, 59, 21)
                        'geopotential': dataset.variables['z'][:],  # Geopotential (968, 1, 59, 21)
                        'ozone': dataset.variables['o3'][:],  # Ozone mass mixing ratio (968, 1, 59, 21)
                        'potential_vorticity': dataset.variables['pv'][:],  # Potential vorticity (968, 1, 59, 21)
                        'relative_humidity': dataset.variables['r'][:],  # Relative humidity (968, 1, 59, 21)
                        'cloud_ice_water_content': dataset.variables['ciwc'][:],  # Specific cloud ice water content (968, 1, 59, 21)
                        'cloud_liquid_water_content': dataset.variables['clwc'][:],  # Specific cloud liquid water content (968, 1, 59, 21)
                        'q': dataset.variables['q'][:],  # Specific humidity (968, 1, 59, 21)
                        'rain_water_content': dataset.variables['crwc'][:],  # Specific rain water content (968, 1, 59, 21)
                        'snow_water_content': dataset.variables['cswc'][:],  # Specific snow water content (968, 1, 59, 21)
                        'temperature': dataset.variables['t'][:],  # Temperature (968, 1, 59, 21)
                        'u_component_wind': dataset.variables['u'][:],  # U-component of wind (968, 1, 59, 21)
                        'v_component_wind': dataset.variables['v'][:],  # V-component of wind (968, 1, 59, 21)
                        'vertical_velocity': dataset.variables['w'][:],  # Vertical velocity (968, 1, 59, 21)
                        'relative_velocity': dataset.variables['vo'][:]  # Relative vorticity (968, 1, 59, 21)
                    }
        dataset.close()
        
        # Create meshgrid for all dimensions
        logger.info("Creating dimension meshgrid")
        time_grid, level_grid, lat_grid, lon_grid = np.meshgrid(
            valid_time, pressure_level, latitude, longitude, indexing='ij'
        )
        
        # Initialize data dictionary with dimensions
        data = {
            'valid_time': time_grid.flatten(),
            'pressure_level': level_grid.flatten(),
            'latitude': lat_grid.flatten(),
            'longitude': lon_grid.flatten()
        }
        
        # Process each variable
        logger.info("Processing variables")
        for var_name, var_data in tqdm(variables.items(), desc="Flattening variables"):
            if var_name not in ['valid_time', 'pressure_level', 'latitude', 'longitude']:
                expected_shape = (len(valid_time), len(pressure_level), len(latitude), len(longitude))
                
                if var_name == 'expver':
                    # Handle expver differently as it may have a different shape
                    data[var_name] = np.repeat(var_data, len(pressure_level) * len(latitude) * len(longitude))
                elif var_data.shape == expected_shape:
                    data[var_name] = var_data.flatten()
                else:
                    logger.warning(f"Variable {var_name} has unexpected shape: {var_data.shape}, expected: {expected_shape}")
        
        # Create DataFrame and add geometry
        logger.info("Creating DataFrame")
        df = pd.DataFrame(data)
        
        # # Add geometry column for GIS applications
        # df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
        
        # Remove 'q' column.
        if 'q' in df.columns:
            df.drop(columns=['q'], inplace=True)
        
        # Convert timestamps to datetime
        logger.info("Converting timestamps and splitting data into train/test sets")
        dates = pd.to_datetime(df["valid_time"], unit="s")
        
        # Define date ranges for train/test public/private splitting
        date_ranges = {
            "public_train": (datetime(2015, 1, 1), datetime(2020, 12, 31)),
            "public_test": (datetime(2021, 1, 1), datetime(2022, 12, 31)),
            "train": (datetime(2015, 1, 1), datetime(2022, 12, 31)),
            "test": (datetime(2023, 1, 1), datetime.now())
        }
        
        # Save the datasets based on date ranges
        for name, (start_date, end_date) in tqdm(date_ranges.items(), desc="Saving datasets"):
            mask = (dates >= start_date) & (dates <= end_date)
            subset = df.loc[mask]
            
            if "public" in name:
                output_path = f"{output_dir}/public/{name.split('_')[1]}.csv"
            else:
                output_path = f"{output_dir}/{name}.csv"
            
            if len(subset) > 0:
                logger.info(f"Saving {name} dataset with {len(subset)} rows to {output_path}")
                subset.to_csv(output_path, index=False)
            else:
                logger.warning(f"No data found for {name} dataset in date range {start_date} to {end_date}")
        
        logger.info("Data preparation completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    file_path = './Data_extraction/91876b95c55af324dff8f275ebb8d589.nc'
    prepare_climate_data(file_path)