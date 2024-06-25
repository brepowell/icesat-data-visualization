# Breanna Powell
# Started 06/25/2024
# Modified from https://icepyx.readthedocs.io/en/latest/example_notebooks/IS2_data_visualization.html

##########
# TO RUN #
##########

# Libraries required:
# https://pypi.org/project/icepyx/

# Icepyx dependencies under the hood: • fiona • GeoPandas • Pangeo 11icepyx • shapely • xarray
# https://icepyx.readthedocs.io/_/downloads/en/stable/pdf/

# Have e3sm-data-practice-visualization.py in the same directory

import icepyx as ipx
from e3sm_data_practice_visualization import *

##########################################################
# VARIABLES FOR CREATING A BOUNDING BOX TO VIEW THE DATA #
##########################################################

# See this for more info about the variables: 
# https://icepyx.readthedocs.io/en/latest/example_notebooks/IS2_data_access.html
    # SHORT_NAME is the data of interest
    # spatial_extent is the bounding box. It can be a shp, kml, or gpkg format for a polygon shape
    # date_range is in the format YYYY-MM-DD, or it can be a list of 2 datetime objects
    # cycles is what orbital cycle to use; can be left blank to collect all possible in the search parameters
    # tracks are the laser tracks.

# SHORT_NAME variable possibilities: 
# https://nsidc.org/data/icesat-2/products
    # ATL07 is Sea Ice Height
    # ATL06 is Land Ice Height
    # ATL10 is Sea Ice Freeboard ** what we are interested in **
SHORT_NAME = 'ATL10'

# spatial_extent examples, using a rectangle, polygon, or a shape file:
    # Decimal degrees for the lower left longitude, lower left latitude, 
    #                         upper right longitude, and upper right latitude

    #       ---------X
    #       |        |
    #       |        |
    #       |        |
    #       X---------

    # rectangle_spatial_extent = [-67, -70, -59, -65] 
    # polygon_spatial_extent = [(-55, 68), (-55, 71), (-48, 71), (-48, 68), (-55, 68)]
    # polygon_file_spatial_extent = './supporting_files/data-access_PineIsland/glims_polygons.shp'

# Bounding Box
LOWER_LEFT_LONGITUDE    = 180
LOWER_LEFT_LATITUDE     = 50
UPPER_RIGHT_LONGITUDE   = -180
UPPER_RIGHT_LATITUDE    = 50

spatial_extent  = [LOWER_LEFT_LONGITUDE, LOWER_LEFT_LATITUDE, UPPER_RIGHT_LONGITUDE, UPPER_RIGHT_LATITUDE]
# tracks. See https://icesat-2.gsfc.nasa.gov/science/specs

date_range      = ['2020-7-1', '2020-7-2'] # YYYY-MM-DD
start_time      = '03:30:00'
end_time        = '21:30:00'

# Use the parameters that you specified to query the database for that area in that date range
region = ipx.Query(SHORT_NAME, spatial_extent, date_range, start_time, end_time)

def printDetails(region):
    print(region.product)
    print(region.dates)
    print(region.start_time)
    print(region.end_time)
    print(region.product_version)
    print(list(set(region.avail_granules(cycles=True)[0]))) #region.cycles
    print(list(set(region.avail_granules(tracks=True)[0]))) #region.tracks

def downloadSatelliteData(region):
    #path = './satellite_data'
    #region.download_granules(path)
    region.order_granules(format='NetCDF4-CF')

def main():
    printDetails(region)

if __name__ == "__main__":
    main()
