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

# ValueError: Invalid keyword: longitude. 
# Please select from this list: ancillary_data, freeboard_estimation, freeboard_segment, geophysical, gt1l, gt1r, gt2l, gt2r, gt3l, gt3r, heights, leads, none, orbit_info, quality_assessment, reference_surface_section
KEYWORDSFORSUBSET = ['freeboard_estimation', 'freeboard_segment'] # This is what variables you want to collect from ICESAT-2

VARIABLESTOGRAB = ['longitude', 'latitude', 'beam_fb_height'] 

def printQueryDetails(region_a):
    """ This helps you narrow down your query to a good range. 
    Ideally, you do not want to plot a lot of tracks. """
    print("Queried for ",     PRODUCTS[region_a.product])
    print("Spatial Extent: ", region_a.spatial_extent[1])
    print("Date Range:     ", region_a.dates)
    print("Start Time:     ", region_a.start_time)
    print("End Time:       ", region_a.end_time)
    print("Version:        ", region_a.product_version)
    print("Cycles:         ", list(set(region_a.avail_granules(cycles=True)[0]))) #region_a.cycles
    print("Tracks:         ", list(set(region_a.avail_granules(tracks=True)[0]))) #region_a.tracks


def subsetTheData(region_a, printResult=True):

    a = region_a.order_vars.wanted
    region_a.order_vars.append(keyword_list=KEYWORDSFORSUBSET)
    
    if printResult==True:
        print(region_a.order_vars.wanted)

def queryForSatelliteAtSpaceAndTime(printResult=True):
    """ Query for only one location and a specific time. ICESat-2 lauched on September 15, 2018, 
    so do not expect to be able to see data earlier than that. Use a bounding box or other shape to query
    for a certain spatial extent. """
    spatial_extent  = [LOWER_LEFT_LONGITUDE, LOWER_LEFT_LATITUDE, UPPER_RIGHT_LONGITUDE, UPPER_RIGHT_LATITUDE]
    date_range      = ['2020-2-28', '2020-2-29'] # YYYY-MM-DD
    start_time      = '15:00:00'
    end_time        = '20:00:00'

    # Use the parameters that you specified to query the database for that area in that date range
    region_a = ipx.Query(SHORT_NAME, spatial_extent, date_range, start_time, end_time, tracks=TRACKS)
    # region_a = ipx.Query(SHORT_NAME, spatial_extent, date_range) # Use default start and end times.

    # Hard-Coded Example
    # region_a = ipx.Query('ATL06',[-55, 68, -48, 71],['2019-02-22','2019-02-28'], start_time='00:00:00', end_time='23:59:59')

    if printResult==True:
        printQueryDetails(region_a)

    return region_a

def seeAvailableVariables(region_a):
    import sys, io

    filename = "variables.txt"
    with open(filename, 'w') as file:
        # Create a string buffer to capture the printed output
        buffer = io.StringIO()
        # Redirect standard output to the buffer
        sys.stdout = buffer
        
        # Call the function that prints its output
        region_a.show_custom_options(dictview=True)
        
        # Restore the standard output
        sys.stdout = sys.__stdout__
        
        # Get the content of the buffer
        output = buffer.getvalue()
        
        if output:
            file.write(output)
        else:
            print("Error: The output of show_custom_options is None or empty.")

# https://icepyx.readthedocs.io/en/latest/example_notebooks/IS2_data_access2-subsetting.html#why-does-the-subsetter-say-no-matching-data-was-found
def downloadSatelliteData(region_a, satelliteDataPath):
    """ Download the data as a netCDF .nc file. """
    region_a.download_granules(path=satelliteDataPath, format='NetCDF4-CF') # Calls order_granules() under the hood

def main():

    ##################################
    # QUERY, PULL, AND SAVE THE DATA #
    ##################################

    satelliteDataPath = '/satellite_data'

    # region_a = queryForSatelliteAtSpaceAndTime()        # Can set printResult to be False
    # subsetTheData(region_a, False)                      # Can set printResult to be False
    # seeAvailableVariables(region_a) # Saves the big long list of variables into variables.txt file.
    # downloadSatelliteData(region_a, satelliteDataPath) # Only use when you need to download the data

    ################
    # MAP THE DATA #
    ################
    runDir           = os.path.dirname(os.path.abspath(__file__))  # Get current directory path
    
    # Load the mesh and data to plot.
    meshFileName     = r"\netCDF_files\seaice.EC30to60E2r2.210210.nc"
    latCell, lonCell = loadMesh(runDir, meshFileName)

    outputFileName = r"\satellite_data\processed_ATL10-01_20200228162543_09770601_006_01.nc"  # .nc file for the data to plot    
    variableToPlot1D = loadData(runDir, outputFileName, VARIABLESTOGRAB[2])
    mapImageFileName = 'satellite_Output.png'

    generateNorthandSouthPoleMaps(latCell, lonCell, variableToPlot1D, mapImageFileName, 1,1,1,1)

if __name__ == "__main__":
    main()
