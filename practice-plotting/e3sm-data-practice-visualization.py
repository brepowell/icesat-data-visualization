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
import math
import numpy as np
import xarray
import matplotlib.path as mpath
import matplotlib.pyplot as plt

# Cartopy for map features, like land and ocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Constants
MAXLONGITUDE = 180
MINLONGITUDE = -180
NORTHPOLE = 90
LAT_LIMIT = 50

# Change these for different runs
runDir = os.path.dirname(os.path.abspath(__file__))     # Gets the current directory path
meshFileName = "\data\seaice.EC30to60E2r2.210210.nc"                                         # .nc file for the mesh
outputFileName = "\data\Breanna_D_test_1.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot
varToPlot = 'timeDaily_avg_iceAreaCell' # The variable that you want to plot

def loadMesh(runDir, meshFileName):
    """ Load the mesh from an .nc file. The mesh must have the same resolution as the output file. """
    print('read: ', runDir, meshFileName)
    mesh = xarray.open_dataset(runDir + meshFileName)
    nCells = mesh.sizes['nCells']
    latCell = mesh.variables['latCell'] # in radians
    lonCell = mesh.variables['lonCell']
    xCell = mesh.variables['xCell'] # in meters
    yCell = mesh.variables['yCell']
    return nCells, latCell, lonCell, xCell, yCell

def loadData(runDir, outputFileName):
    """ Load the data from an .nc output file. Returns a 1D array of the variable you want to plot. """
    print('read: ', runDir, outputFileName)
    output = xarray.open_dataset(runDir + outputFileName)
    var = output.variables[varToPlot]
    var1D = var[0,:] # reduce the variable to 1D so we can use these indices
    return var1D

def mapHemisphere(latCell, xCell, yCell, var1D, hemisphere, title, hemisphereMap):
    """ Map one hemisphere onto a matplotlib figure. 
    You do not need to include the minus sign if mapping southern hemisphere. """
    if hemisphere == "n":
        indices = np.where(latCell > math.radians(LAT_LIMIT))
    elif hemisphere == "s":
        indices = np.where(latCell < math.radians(-LAT_LIMIT))

    sc = hemisphereMap.scatter(xCell[indices], yCell[indices], c=var1D[indices], cmap='bwr', s=0.4)
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

def generateNorthandSouthPoleMaps():
    """ Generate 2 maps; one of the north pole and one of the south pole. """
    fig = plt.figure(figsize=[10, 5])
    leftMap = fig.add_subplot(1, 2, 1, projection=ccrs.NorthPolarStereo())
    rightMap = fig.add_subplot(1, 2, 2, projection=ccrs.SouthPolarStereo(),
                            sharex=leftMap, sharey=leftMap)

    # Adjusts the margins around the plots (as a fraction of the width or height)
    fig.subplots_adjust(bottom=0.05, top=0.95,
                        left=0.04, right=0.95, wspace=0.02)

    # Format for set_extent is [minimum longitude, maximum longitude, minimum latitude, maximum latitude]
    leftMap.set_extent([MINLONGITUDE, MAXLONGITUDE, LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())

    leftMap.add_feature(cfeature.OCEAN)
    rightMap.add_feature(cfeature.OCEAN)

    leftMap.add_feature(cfeature.LAND)
    rightMap.add_feature(cfeature.LAND)

    leftMap.gridlines()
    rightMap.gridlines()

    # Crops the map to be round instead of rectangular
    rightMap.set_boundary(makeCircle(), transform=rightMap.transAxes)
    leftMap.set_boundary(makeCircle(), transform=leftMap.transAxes)

    nCells, latCell, lonCell, xCell, yCell = loadMesh(runDir, meshFileName)
    var1D = loadData(runDir, outputFileName)
    mapHemisphere(latCell, xCell, yCell, var1D, "n", "Arctic Sea Ice", leftMap)      # Map northern hemisphere
    mapHemisphere(latCell, xCell, yCell, var1D, "s", "Antarctic Sea Ice", rightMap) # Map southern hemisphere

    plt.savefig('seaice_Output.png')

generateNorthandSouthPoleMaps()