# Author:   Breanna Powell
# Date:     07/15/2024

##########
# TO RUN #
##########

# Use the config.py file to specify max latitude, max longitude, file paths, etc.
# Make sure that you navigate to the directory that contains plotting_track_animation_over_time.py
# Make sure that the e3sm_data_visualization.py file is also in the same directory.
# Make sure that plotting_track_animation.py is in the same directory.
# Make sure that utility.py is in the same directory.

# $ python plotting_track_animation_over_time.py

# Takes 30-60 seconds for plotting a day
# Takes 3218 seconds or 53 minutes for plotting a week (without downsampling)
# TODO: Add a downsampling option to speed up the process

import matplotlib.animation as animation
from e3sm_data_visualization import *
from utility import *
from plotting_track_animation import *

import time
import os

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