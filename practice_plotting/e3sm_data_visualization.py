# Author:   Breanna Powell
# Date:     07/02/2024

##########
# TO RUN #
##########

# Use the config.py file to specify max latitude, max longitude, file paths, etc.
# Ensure that you are looking for a variable that exists in the output file
# Make sure that you navigate to the directory that contains e3sm-data-visualization.py
# Make sure that utility.py is in the same directory

# $ python e3sm-data-visualization.py

import matplotlib.path as mpath
import matplotlib.pyplot as plt     # For plotting

# Cartopy for map features, like land and ocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from utility import *

def mapNorthernHemisphere(latCell, lonCell, variableToPlot1Day, title, hemisphereMap, dot_size=DOT_SIZE):
    """ Map the northern hemisphere onto a matplotlib figure. 
    This requires latCell and lonCell to be filled by a mesh file.
    It also requires variableToPlot1Day to be filled by an output .nc file. """

    indices = np.where(latCell > LAT_LIMIT)     # Only capture points between the lat limit and the pole.
    
    norm=mpl.colors.Normalize(VMIN, VMAX)
    sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], 
                               c=variableToPlot1Day[indices], cmap='bwr', 
                               s=dot_size, transform=ccrs.PlateCarree(),
                               norm=norm)
    hemisphereMap.set_title(title)
    hemisphereMap.axis('off')

    return sc

def mapInOneColorLatsAndLons(latCell, lonCell, title, hemisphereMap, dot_size=DOT_SIZE):
    """ Map the northern hemisphere onto a matplotlib figure. 
    This requires latCell and lonCell to be filled by a mesh file.
    It also requires variableToPlot1Day to be filled by an output .nc file. """

    indices = np.where(latCell > LAT_LIMIT)     # Only capture points between the lat limit and the pole.
    
    norm=mpl.colors.Normalize(VMIN, VMAX)
    sc = hemisphereMap.scatter(lonCell[indices], latCell[indices],
                               s=dot_size, color = 'hotpink', transform=ccrs.PlateCarree(),
                               norm=norm)
    hemisphereMap.set_title(title)
    hemisphereMap.axis('off')

    return sc

def mapSouthernHemisphere(latCell, lonCell, variableToPlot1Day, title, hemisphereMap, dot_size=DOT_SIZE):
    """ Map one hemisphere onto a matplotlib figure. 
    You do not need to include the minus sign for lower latitudes. 
    This requires latCell and lonCell to be filled by a mesh file.
    It also requires variableToPlot1Day to be filled by an output .nc file. """

    indices = np.where(latCell < -LAT_LIMIT)    # Only capture points between the lat limit and the pole.
    
    norm=mpl.colors.Normalize(VMIN, VMAX)
    sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], 
                               c=variableToPlot1Day[indices], cmap='bwr', 
                               s=dot_size, transform=ccrs.PlateCarree(),
                               norm=norm)
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

def addMapFeatures(my_map, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES):
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

def generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, 
                                  timeStamp="YYYY:DD:HH:MM", colorBarOn=COLORBARON, grid=GRIDON,
                                  oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, 
                                  coastlines=COASTLINES, dot_size=DOT_SIZE):
    """ Generate 2 maps; one of the north pole and one of the south pole. """

    # Adjust the margins around the plots (as a fraction of the width or height).
    fig.subplots_adjust(bottom=0.05, top=0.85, left=0.04, right=0.95, wspace=0.02)

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
    northPoleScatter = mapNorthernHemisphere(latCell, lonCell, variableToPlot1Day, "Arctic Sea Ice", northMap, dot_size=dot_size)     # Map northern hemisphere
    southPoleScatter = mapSouthernHemisphere(latCell, lonCell, variableToPlot1Day, "Antarctic Sea Ice", southMap, dot_size=dot_size)  # Map southern hemisphere

    # Set Color Bar
    if colorBarOn:
        plt.colorbar(northPoleScatter, ax=northMap)
        plt.colorbar(southPoleScatter, ax=southMap)

    # Add time textbox
    plt.suptitle(MAP_SUPTITLE_TOP, size="x-large", fontweight="bold")

    # Save the maps as an image.
    #plt.savefig(mapImageFileName) # TODO: ADD THIS BACK IN. TRYING TO SAVE TIME ON PLOTTING 1 YEAR

    return northPoleScatter, southPoleScatter

def generateNorthPoleMap(fig, northMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, 
                         timeStamp="YYYY:DD:HH:MM", colorBarOn=COLORBARON, grid=GRIDON,
                         oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, 
                         coastlines=COASTLINES, dot_size=DOT_SIZE):
    """ Generate one map of the north pole. """

    # Adjust the margins around the plots (as a fraction of the width or height).
    fig.subplots_adjust(bottom=0.05, top=0.85, left=0.04, right=0.95, wspace=0.02)

    # Set your viewpoint (the bounding box for what you will see).
    # You want to see the full range of longitude values, since this is a polar plot.
    # The range for the latitudes should be from your latitude limit (i.e. 50 degrees or -50 to the pole at 90 or -90).
    northMap.set_extent([MINLONGITUDE, MAXLONGITUDE, LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())

    # Add map features, like landFeature and oceanFeature.
    addMapFeatures(northMap, oceanFeature, landFeature, grid, coastlines)

    # Crop the map to be round instead of rectangular.
    northMap.set_boundary(makeCircle(), transform=northMap.transAxes)

    # Map the hemisphere
    scatter = mapNorthernHemisphere(latCell, lonCell, variableToPlot1Day, f"Arctic Sea Ice", northMap, dot_size)     # Map northern hemisphere
    
    # Set Color Bar
    if colorBarOn:
        plt.colorbar(scatter, ax=northMap)

    plt.suptitle(MAP_SUPTITLE_TOP, size="x-large", fontweight="bold")

    # Save the maps as an image.
    plt.savefig(mapImageFileName)

    return scatter

def main():

    # Load the mesh and data to plot.
    #latCell, lonCell = loadMesh(runDir, meshFileName)
    latCell, lonCell = loadMesh("", meshFileName)
    output = loadData(runDir, outputFileName)

    ####################################################
    # PLOTTING REGULAR E3SM OUTPUT DATA, LIKE ICE AREA #
    ####################################################
    #print("Days total: ", getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT))
    #variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=1)
    
    ##############################
    # PLOTTING MY NEW.NC RESULTS #
    ##############################
    print("nCells total: ", getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT))
    variableToPlot1Day = output.variables[VARIABLETOPLOT][:]
    variableToPlot1Day.ravel()
    print(variableToPlot1Day.shape)

    #######################
    # NORTH & SOUTH POLES #
    #######################
    #fig, northMap, southMap = generateNorthandSouthPoleAxes()
    #generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, "seaice_both_poles", dot_size=0.4)

    ###################
    # ARTIC-ONLY PLOT #
    ###################
    fig, northMap = generateNorthPoleAxes()

    # Plotting with a variable
    generateNorthPoleMap(fig, northMap, latCell, lonCell, variableToPlot1Day, mapImageFileName)
    #mapInOneColorLatsAndLons(latCell, lonCell, mapImageFileName, dot_size=0.4)

if __name__ == "__main__":
    main()