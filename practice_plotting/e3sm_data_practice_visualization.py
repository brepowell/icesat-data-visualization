# Author:   Breanna Powell
# Date:     07/02/2024

##########
# TO RUN #
##########

# Make sure that you navigate to the directory that contains e3sm-data-practice-visualization.py
# Have a folder labeled "netCDF_files" in that directory
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
MAXLONGITUDE    =  180
MINLONGITUDE    = -180
NORTHPOLE       =  90
SOUTHPOLE       = -90
LAT_LIMIT       =  50  # Good wide view for the north and south poles; change if you want a wider or narrower view.
VARIABLETOPLOT  = 'timeDaily_avg_iceAreaCell'   # The variable to plot

def loadMesh(runDir, meshFileName):
    """ Load the mesh from an .nc file. The mesh must have the same resolution as the output file. """
    print('read: ', runDir, meshFileName)

    dataset = netCDF4.Dataset(runDir + meshFileName)
    latCell = np.degrees(dataset.variables['latCell'][:]) # Convert from radians to degrees.
    lonCell = np.degrees(dataset.variables['lonCell'][:]) # Convert from radians to degrees.

    return latCell, lonCell

def loadData(runDir, outputFileName):
    """ Load the data from an .nc output file. Returns a 1D array of the variable you want to plot of size nCells.
    The indices of the 1D array match with those of the latitude and longitude arrays, which are also size nCells."""
    print('read: ', runDir, outputFileName)

    return netCDF4.Dataset(runDir + outputFileName)

def printAllAvailableVariables(output):
    """ See what variables you can use in this netCDF file. 
    Requires having loaded a netCDF file into an output variable. """
    print(output.variables) # See all variables available in the netCDF file

def getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT):
    """ Find out how many days are in the simulation by looking at the netCDF file and at the variable
     you have chosen to plot. """
    variableForAllDays = output.variables[keyVariableToPlot][:]
    return variableForAllDays.shape[0]

def reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0):
    """ Reduce the variable to one day's worth of data so we can plot using each indice per cell. 
        The indices for each cell of the variableToPlot1Day array coincide with the indices 
        of the latCell and lonCell. """
    
    variableForAllDays = output.variables[keyVariableToPlot][:]
    variableToPlot1Day = variableForAllDays[dayNumber,:]                                     
    # print("variableToPlot1Day", variableToPlot1Day[0:5])

    return variableToPlot1Day

def mapHemisphere(latCell, lonCell, variableToPlot1Day, hemisphere, title, hemisphereMap):
    """ Map one hemisphere onto a matplotlib figure. 
    You do not need to include the minus sign if mapping southern hemisphere. 
    This requires latCell and lonCell to be filled by a mesh file.
    It also requires variableToPlot1Day to be filled by an output .nc file. """
    if hemisphere == "n":
        indices = np.where(latCell > LAT_LIMIT)     # Only capture points between the lat limit and the pole.
    elif hemisphere == "s":
        indices = np.where(latCell < -LAT_LIMIT)    # Only capture points between the lat limit and the pole.
    else:
        return
    
    sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], c=variableToPlot1Day[indices], cmap='bwr', s=0.4, transform=ccrs.PlateCarree())
    hemisphereMap.set_title(title)
    hemisphereMap.axis('off')

    return sc

def makeCircle():
    """ Use this with Cartopy to make a circular map of the globe, 
    rather than a rectangular map. """
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    return mpath.Path(verts * radius + center)

def addMapFeatures(my_map, oceanFeature=1, landFeature=1, grid=1, coastlines=1):
    """ Set optional features on the map """
    if (oceanFeature == 1):
        my_map.add_feature(cfeature.OCEAN)

    if (landFeature == 1):
        my_map.add_feature(cfeature.LAND)

    if (grid == 1):
        my_map.gridlines()

    if (coastlines == 1):
        my_map.coastlines()

def generateNorthandSouthPoleAxes():
    """ Return a figure and axes (maps) to use for plotting data for the North and South Poles. """
    fig = plt.figure(figsize=[10, 5]) #both north and south pole
    
    # Define projections for each map.
    map_projection_north = ccrs.NorthPolarStereo(central_longitude=270, globe=None)
    map_projection_south = ccrs.SouthPolarStereo(central_longitude=0, globe=None)

    # Create the two maps as subplots of the figure.
    northMap = fig.add_subplot(1, 2, 1, projection=map_projection_north)
    southMap = fig.add_subplot(1, 2, 2, projection=map_projection_south)

    return fig, northMap, southMap

def generateNorthPoleAxes():
    """ Return a figure and axes (map) to use for plotting data for the North Pole. """

    fig = plt.figure(figsize=[5, 5]) #north pole only
    
    # Define projections for each map.
    map_projection_north = ccrs.NorthPolarStereo(central_longitude=270, globe=None)
    
    # Create an axes for a map of the Arctic on the figure
    northMap = fig.add_subplot(1, 1, 1, projection=map_projection_north)
    return fig, northMap

def generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, colorBarOn=1, oceanFeature=1, landFeature=1, grid=1, coastlines=1):
    """ Generate 2 maps; one of the north pole and one of the south pole. """

    # Adjust the margins around the plots (as a fraction of the width or height).
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

    # Set your viewpoint (the bounding box for what you will see).
    # You want to see the full range of longitude values, since this is a polar plot.
    # The range for the latitudes should be from your latitude limit (i.e. 50 degrees or -50 to the pole at 90 or -90).
    northMap.set_extent([MINLONGITUDE, MAXLONGITUDE,  LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())
    southMap.set_extent([MINLONGITUDE, MAXLONGITUDE, -LAT_LIMIT, SOUTHPOLE], ccrs.PlateCarree())

    # Add map features, like landFeature and oceanFeature.
    addMapFeatures(northMap, oceanFeature, landFeature, grid, coastlines)
    addMapFeatures(southMap, oceanFeature, landFeature, grid, coastlines)

    # Crop the map to be round instead of rectangular.
    northMap.set_boundary(makeCircle(), transform=northMap.transAxes)
    southMap.set_boundary(makeCircle(), transform=southMap.transAxes)

    # Map the 2 hemispheres.
    northPoleScatter = mapHemisphere(latCell, lonCell, variableToPlot1Day, "n", "Arctic Sea Ice", northMap)     # Map northern hemisphere
    southPoleScatter = mapHemisphere(latCell, lonCell, variableToPlot1Day, "s", "Antarctic Sea Ice", southMap)  # Map southern hemisphere

    # Set Color Bar
    if colorBarOn:
        plt.colorbar(northPoleScatter, ax=northMap)
        plt.colorbar(southPoleScatter, ax=southMap)

    # Save the maps as an image.
    plt.savefig(mapImageFileName)

    return northPoleScatter, southPoleScatter

def generateNorthPoleMap(fig, northMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, colorBarOn=1, oceanFeature=1, landFeature=1, grid=1, coastlines=1):
    """ Generate 2 maps; one of the north pole and one of the south pole. """

    # Adjust the margins around the plots (as a fraction of the width or height).
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

    # Set your viewpoint (the bounding box for what you will see).
    # You want to see the full range of longitude values, since this is a polar plot.
    # The range for the latitudes should be from your latitude limit (i.e. 50 degrees or -50 to the pole at 90 or -90).
    northMap.set_extent([MINLONGITUDE, MAXLONGITUDE, LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())

    # Add map features, like landFeature and oceanFeature.
    addMapFeatures(northMap, oceanFeature, landFeature, grid, coastlines)

    # Crop the map to be round instead of rectangular.
    northMap.set_boundary(makeCircle(), transform=northMap.transAxes)

    # Map thehemispheres.
    scatter = mapHemisphere(latCell, lonCell, variableToPlot1Day, "n", "Arctic Sea Ice", northMap)     # Map northern hemisphere

    # Set Color Bar
    if colorBarOn:
        plt.colorbar(scatter, ax=northMap)

    # Save the maps as an image.
    plt.savefig(mapImageFileName)

    return scatter

def main():

    # Change these for different runs
    runDir         = os.path.dirname(os.path.abspath(__file__))                                  # Get current directory path
    meshFileName   = r"\netCDF_files\seaice.EC30to60E2r2.210210.nc"                                       # .nc file for the mesh
    outputFileName = r"\netCDF_files\Breanna_D_test_1.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot

    # Load the mesh and data to plot.
    latCell, lonCell = loadMesh(runDir, meshFileName)
    output = loadData(runDir, outputFileName)
    print("Days total: ", getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT))
    variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=1)
    
    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, "seaice_both_poles", 1,1,1,1,1)

    # Plot just the arctic
    fig, northMap = generateNorthPoleAxes()
    generateNorthPoleMap(fig, northMap, latCell, lonCell, variableToPlot1Day, "seaice_north_pole", 1,1,1,1,1)

if __name__ == "__main__":
    main()