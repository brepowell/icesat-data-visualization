# Breanna Powell
# Modified code from Mark Petersen and Savannah Byron

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
MAXLONGITUDE =  180
MINLONGITUDE = -180
NORTHPOLE    =  90
SOUTHPOLE    = -90
LAT_LIMIT    =  50  # Good wide view for the north and south poles; change if you want a wider or narrower view.

# Change these for different runs
runDir         = os.path.dirname(os.path.abspath(__file__))                                  # Get current directory path
meshFileName   = r"\netCDF_files\seaice.EC30to60E2r2.210210.nc"                                       # .nc file for the mesh
outputFileName = r"\netCDF_files\Breanna_D_test_1.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot
keyVariableToPlot      = 'timeDaily_avg_iceAreaCell'                                                 # The variable to plot

def loadMesh(runDir, meshFileName):
    """ Load the mesh from an .nc file. The mesh must have the same resolution as the output file. """
    print('read: ', runDir, meshFileName)

    dataset = netCDF4.Dataset(runDir + meshFileName)
    latCell = np.degrees(dataset.variables['latCell'][:]) # Convert from radians to degrees.
    lonCell = np.degrees(dataset.variables['lonCell'][:]) # Convert from radians to degrees.

    return latCell, lonCell

def loadData(runDir, outputFileName, keyVariableToPlot):
    """ Load the data from an .nc output file. Returns a 1D array of the variable you want to plot of size nCells.
    The indices of the 1D array match with those of the latitude and longitude arrays, which are also size nCells."""
    print('read: ', runDir, outputFileName)

    # Load the data into a variable named "output"
    output = netCDF4.Dataset(runDir + outputFileName)
    var = output.variables[keyVariableToPlot][:]

    # Reduce the variable to 1D so we can use the indices.
    # The indices for each cell of the variableToPlot1D array coincide with the indices of the latCell and lonCell.
    variableToPlot1D = var[0,:]                                      
    print("variableToPlot1D", variableToPlot1D[0:5])

    return variableToPlot1D

def mapHemisphere(latCell, lonCell, variableToPlot1D, hemisphere, title, hemisphereMap):
    """ Map one hemisphere onto a matplotlib figure. 
    You do not need to include the minus sign if mapping southern hemisphere. 
    This requires latCell and lonCell to be filled by a mesh file.
    It also requires variableToPlot1D to be filled by an output .nc file. """
    if hemisphere == "n":
        indices = np.where(latCell > LAT_LIMIT)     # Only capture points between the lat limit and the pole.
    elif hemisphere == "s":
        indices = np.where(latCell < -LAT_LIMIT)    # Only capture points between the lat limit and the pole.
    else:
        return
    
    sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], c=variableToPlot1D[indices], cmap='bwr', s=0.4, transform=ccrs.PlateCarree())
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

def generateNorthandSouthPoleMaps(latCell, lonCell, variableToPlot1D, mapImageFileName, oceanFeature=1, landFeature=1, grid=1, coastlines=1):
    """ Generate 2 maps; one of the north pole and one of the south pole. """
    fig = plt.figure(figsize=[10, 5])

    # Define projections for each map.
    map_projection_north = ccrs.NorthPolarStereo(central_longitude=270, globe=None)
    map_projection_south = ccrs.SouthPolarStereo(central_longitude=0, globe=None)

    # Create the two maps as subplots of the figure.
    northMap = fig.add_subplot(1, 2, 1, projection=map_projection_north)
    southMap = fig.add_subplot(1, 2, 2, projection=map_projection_south)

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
    mapHemisphere(latCell, lonCell, variableToPlot1D, "n", "Arctic Sea Ice", northMap)     # Map northern hemisphere
    mapHemisphere(latCell, lonCell, variableToPlot1D, "s", "Antarctic Sea Ice", southMap)  # Map southern hemisphere

    # Save the maps as an image.
    plt.savefig(mapImageFileName)

def main():

    # Load the mesh and data to plot.
    latCell, lonCell = loadMesh(runDir, meshFileName)
    variableToPlot1D = loadData(runDir, outputFileName, keyVariableToPlot)
    mapImageFileName = 'seaice_Output.png'

    generateNorthandSouthPoleMaps(latCell, lonCell, variableToPlot1D, mapImageFileName, 1,1,1,1)

if __name__ == "__main__":
    main()