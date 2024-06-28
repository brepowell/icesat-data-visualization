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
import pprint # Pretty print library to print the variables nicely
from e3sm_data_practice_visualization import *

######################
# ALL ABOUT ICESAT-2 #
######################

    # Basic info about IceSat-2:    https://nsidc.org/data/icesat-2
    # More info about the data:     https://openaltimetry.earthdatacloud.nasa.gov/data/

    # Interactive site to look at the data: https://openaltimetry.earthdatacloud.nasa.gov/data/icesat2/
    # You can see all the possible tracks to select per day.
    # Example from that site, when looking at Sea Ice Freeboard
    # PHOTON DATA FOR SEGMENT 323566
    # Latitude: 83.821, Longitude: -100.921, Elevation: 0.0955489
    # Time: 2019-12-26 00:02:45.943, Track ID: 1376, Beam: gt2r

    # Example Visuals: 
    # https://svs.gsfc.nasa.gov/4734/ 
    # https://svs.gsfc.nasa.gov/4373/ Shows the orbit

#################################
# VARIABLES FOR AN ICESAT QUERY #
#################################

# See this documentation for more info about the variables: 
# https://icepyx.readthedocs.io/en/latest/example_notebooks/IS2_data_access.html
    # SHORT_NAME is the data of interest
    # spatial_extent is the bounding box. It can be a shp, kml, or gpkg format for a polygon shape
    # date_range is in the format YYYY-MM-DD, or it can be a list of 2 datetime objects
    # cycles is what orbital cycle to use; can be left blank to collect all possible in the search parameters
    # tracks are the laser tracks.

# SHORT_NAME variable possibilities: 
# https://nsidc.org/data/icesat-2/products
    
SHORT_NAME = 'ATL10' # Change this if you want to do different queries

PRODUCTS = {
    "ATL07": "Sea Ice Height",      # ATL07 is Sea Ice Height
    "ATL06": "Land Ice Height",     # ATL06 is Land Ice Height
    "ATL10": "Sea Ice Freeboard"    # ATL10 is Sea Ice Freeboard ** what we are interested in **
}

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
# Originally, I thought 180, 50, -180, 90 
# would give me a good view, but after playing 
# with the interactive OpenAltimetry site, the following gets a good bounding box
LOWER_LEFT_LONGITUDE    = -80
LOWER_LEFT_LATITUDE     = 50
UPPER_RIGHT_LONGITUDE   = 110
UPPER_RIGHT_LATITUDE    = 80

TRACKS = ['0977']     # See https://icesat-2.gsfc.nasa.gov/science/specs

def printQueryDetails(region):
    """ This helps you narrow down your query to a good range. 
    Ideally, you do not want to plot a lot of tracks. """
    print("Queried for ",     PRODUCTS[region.product])
    print("Spatial Extent: ", region.spatial_extent[1])
    print("Date Range:     ", region.dates)
    print("Start Time:     ", region.start_time)
    print("End Time:       ", region.end_time)
    print("Version:        ", region.product_version)
    print("Cycles:         ", list(set(region.avail_granules(cycles=True)[0]))) #region.cycles
    print("Tracks:         ", list(set(region.avail_granules(tracks=True)[0]))) #region.tracks

def getSubsetOfSatData(print=True):

    """ Query for only a small subset of the data, using the time constraints to narrow it down. 
    ICESat-2 lauched on September 15, 2018, so do not expect to be able to see data earlier than that. """
    spatial_extent  = [LOWER_LEFT_LONGITUDE, LOWER_LEFT_LATITUDE, UPPER_RIGHT_LONGITUDE, UPPER_RIGHT_LATITUDE]
    date_range      = ['2020-2-28', '2020-2-29'] # YYYY-MM-DD
    start_time      = '15:00:00'
    end_time        = '20:00:00'

    # Use the parameters that you specified to query the database for that area in that date range
    region = ipx.Query(SHORT_NAME, spatial_extent, date_range, start_time, end_time, tracks=TRACKS)
    # region = ipx.Query(SHORT_NAME, spatial_extent, date_range) # Use default start and end times.

    # Hard-Coded Example
    # region = ipx.Query('ATL06',[-55, 68, -48, 71],['2019-02-22','2019-02-28'], start_time='00:00:00', end_time='23:59:59')

    if print==True:
        printQueryDetails(region)

    return region

def seeAvailableVariables(region):
    import sys, io

    filename = "variables.txt"
    with open(filename, 'w') as file:
        # Create a string buffer to capture the printed output
        buffer = io.StringIO()
        # Redirect standard output to the buffer
        sys.stdout = buffer
        
        # Call the function that prints its output
        region.show_custom_options(dictview=True)
        
        # Restore the standard output
        sys.stdout = sys.__stdout__
        
        # Get the content of the buffer
        output = buffer.getvalue()
        
        if output:
            file.write(output)
        else:
            print("Error: The output of show_custom_options is None or empty.")

# https://icepyx.readthedocs.io/en/latest/example_notebooks/IS2_data_access2-subsetting.html#why-does-the-subsetter-say-no-matching-data-was-found
def downloadSatelliteData(region):
    path = './satellite_data'
    region.download_granules(path=path, format='NetCDF4-CF') # Calls order_granules() under the hood

def main():
    region = getSubsetOfSatData() # Can set print to be False
    # seeAvailableVariables(region) # Saves the big long list of variables into variables.txt file.
    # downloadSatelliteData(region)

if __name__ == "__main__":
    main()
