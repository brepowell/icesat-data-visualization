# Work in progress

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *
from plotting_track_animation import *

import time
import os
import netCDF4

path = runDir + subdirectory

def gatherFiles():
    """ Use the subdirectory specified in the config file. Get all files in that folder. """
    
    filesToPlot = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filesToPlot.append(os.path.join(root, name))

    return filesToPlot

def animateTrackLinesNorthAndSouth(filePaths):
    """ Animates all tracks for a given period of time (one day or one month). 
    Depends on what items are in the specified subdirectory. """
    
    artists = []
    previousTracks = []  # List to keep track of all artists
    fig, northMap, southMap = generateNorthandSouthPoleAxes()

    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    addMapFeatures(southMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
       
    startTime = time.time()

    # Load the mesh and data to plot.
    for file in filePaths:
        # Get data from one file
        output = netCDF4.Dataset(file)
        latCell, lonCell = getLatLon(output)
        satelliteTrack = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)
        
        textBoxString = "Time: " + printDateTime(output)
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)

        # Plot each track for that day
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, 
                                                                           latCell, lonCell, satelliteTrack, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        
        # Allows it to remember all the tracks (not overwrite with each new track)
        previousTracks.extend([northPoleScatter, southPoleScatter, textBox])
        artists.append(list(previousTracks)) 

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=100)

    plt.colorbar(northPoleScatter, ax=northMap)
    plt.colorbar(southPoleScatter, ax=southMap)

    ani.save(filename=animationFileName, writer="pillow")
    print("Saved .gif file")

    endTime = time.time()
    print("It took this much time: ", endTime-startTime)


def animateTrackLinesNorth(filePaths):
    """ Animates all tracks for a given period of time (one day or one month). 
    Depends on what items are in the specified subdirectory. """
    
    artists = []
    previousTracks = []  # List to keep track of all artists
    fig, northMap = generateNorthPoleAxes()

    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)

    startTime = time.time()

    # Load the mesh and data to plot.
    for file in filePaths:
        # Get data from one file
        output = netCDF4.Dataset(file)
        latCell, lonCell = getLatLon(output)
        satelliteTrack = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)
        
        textBoxString = "Time: " + printDateTime(output)
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)

        # Plot each track for that day
        northPoleScatter = generateNorthPoleMap(fig, northMap,
                                                         latCell, lonCell, satelliteTrack, 
                                                         mapImageFileName, 0,0,0,0,0,0)
        
        # Allows it to remember all the tracks (not overwrite with each new track)
        previousTracks.extend([northPoleScatter, textBox])
        artists.append(list(previousTracks)) 

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=100)

    plt.colorbar(northPoleScatter, ax=northMap)

    ani.save(filename=animationFileName, writer="pillow")
    print("Saved .gif file")

    endTime = time.time()
    print("It took this much time: ", endTime-startTime)


def main():
    filePaths = gatherFiles()
    # animateTrackLinesNorthAndSouth(filePaths)
    animateTrackLinesNorth(filePaths)

if __name__ == "__main__":
    main()