# Breanna Powell
# Modified code from Mark Petersen and Savannah Byron

##########
# TO RUN #
##########

# Make sure that you navigate to the directory that contains e3sm-data-practice-visualization.py
# Have a folder labeled "data" in that directory
# The data folder must contain the mesh file and the output file
# Ensure that you are looking for a variable that exists in the output file
# $ python e3sm-data-practice-visualization.py

import os
import numpy as np                  # For working with arrays
import matplotlib.path as mpath
import matplotlib.pyplot as plt     # For plotting
import netCDF4                      # For opening .nc files for numpy

# Cartopy for map features, like land and ocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Constants
MAXLONGITUDE =  180
MINLONGITUDE = -180
NORTHPOLE    =  90
SOUTHPOLE    = -90
LAT_LIMIT    =  50

# Change these for different runs
runDir         = os.path.dirname(os.path.abspath(__file__))                                  # Get current directory path
meshFileName   = "\data\seaice.EC30to60E2r2.210210.nc"                                       # .nc file for the mesh
outputFileName = "\data\Breanna_D_test_1.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot
varToPlot      = 'timeDaily_avg_iceAreaCell'                                                 # The variable to plot

def loadMesh(runDir, meshFileName):
    """ Load the mesh from an .nc file. The mesh must have the same resolution as the output file. """
    print('read: ', runDir, meshFileName)

    dataset = netCDF4.Dataset(runDir + meshFileName)
    latCell = np.degrees(dataset.variables['latCell'][:]) # converted from radians to degrees
    lonCell = np.degrees(dataset.variables['lonCell'][:]) # converted from radians to degrees

    return latCell, lonCell

def loadData(runDir, outputFileName):
    """ Load the data from an .nc output file. Returns a 1D array of the variable you want to plot. """
    print('read: ', runDir, outputFileName)

    output = netCDF4.Dataset(runDir + outputFileName)
    var = output.variables[varToPlot][:]
    var1D = var[0,:]                                      # reduce the variable to 1D so we can use the indices
    print("var1D", var1D[0:5])

    return var1D

def mapHemisphere(latCell, lonCell, var1D, hemisphere, title, hemisphereMap):
    """ Map one hemisphere onto a matplotlib figure. 
    You do not need to include the minus sign if mapping southern hemisphere. """
    if hemisphere == "n":
        indices = np.where(latCell > LAT_LIMIT)
        sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], c=var1D[indices], cmap='bwr', s=0.4, transform=ccrs.PlateCarree())
    elif hemisphere == "s":
        indices = np.where(latCell < -LAT_LIMIT)
        sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], c=var1D[indices], cmap='bwr', s=0.4, transform=ccrs.PlateCarree())
    else:
        return
    
    hemisphereMap.set_title(title)
    hemisphereMap.axis('off')
    plt.colorbar(sc, ax=hemisphereMap)

def makeCircle():
    """ Use this with Cartopy to make a circular map of the globe, 
    rather than a rectangular map. """
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    return mpath.Path(verts * radius + center)

def addMapFeatures(my_map, ocean, land, grid):
    """ Set optional features on the map """
    if (ocean == 1):
        my_map.add_feature(cfeature.OCEAN)

    if (land == 1):
        my_map.add_feature(cfeature.LAND)

    if (grid == 1):
        my_map.gridlines()

    my_map.coastlines()

def generateNorthandSouthPoleMaps(ocean, land, grid):
    """ Generate 2 maps; one of the north pole and one of the south pole. """
    fig = plt.figure(figsize=[10, 5])

    # Define projections for each map
    map_projection_north = ccrs.NorthPolarStereo(central_longitude=270, globe=None)
    map_projection_south = ccrs.SouthPolarStereo(central_longitude=0, globe=None)

    # Create the two maps as subplots of the figure.
    northMap = fig.add_subplot(1, 2, 1, projection=map_projection_north)
    southMap = fig.add_subplot(1, 2, 2, projection=map_projection_south)

    # Adjust the margins around the plots (as a fraction of the width or height)
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

    # Set your viewpoint (the extent)
    northMap.set_extent([MINLONGITUDE, MAXLONGITUDE,  LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())
    southMap.set_extent([MINLONGITUDE, MAXLONGITUDE, -LAT_LIMIT, SOUTHPOLE], ccrs.PlateCarree())

    # Add map features, like land and ocean
    addMapFeatures(northMap, ocean, land, grid)
    addMapFeatures(southMap, ocean, land, grid)

    # Crop the map to be round instead of rectangular.
    northMap.set_boundary(makeCircle(), transform=northMap.transAxes)
    southMap.set_boundary(makeCircle(), transform=southMap.transAxes)

    # Load the mesh, data, and map the 2 hemispheres.
    latCell, lonCell = loadMesh(runDir, meshFileName)
    var1D = loadData(runDir, outputFileName)
    mapHemisphere(latCell, lonCell, var1D, "n", "Arctic Sea Ice", northMap)     # Map northern hemisphere
    mapHemisphere(latCell, lonCell, var1D, "s", "Antarctic Sea Ice", southMap) # Map southern hemisphere

    # Save the maps as an image.
    plt.savefig('seaice_Output.png')

generateNorthandSouthPoleMaps(1,1,1)