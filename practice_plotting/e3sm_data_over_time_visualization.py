# Author:   Breanna Powell
# Date:     07/02/2024

##########
# TO RUN #
##########

# Use the config.py file to specify max latitude, max longitude, file paths, etc.
# Make sure that you navigate to the directory that contains e3sm_data_over_time_visualization.py
# Make sure that the e3sm_data_visualization.py file is also in the same directory.
# Make sure that utility.py is in the same directory

# $ python e3sm_data_over_time_visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from e3sm_data_visualization import *
from utility import *
import time

def saveAnimation(fig, artists, animationFileName, startTime, interval=500):

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=interval)
    ani.save(filename=animationFileName, writer="pillow")
    print("Saved .gif")

    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

def generateArtistsNorthAndSouth(fig, northMap, southMap, latCell, lonCell, output, 
                         mapImageFileName, days, artists, colorBar = True):
    """ This will make a scatter plot and time stamp per timestep of data in one .nc file.
        It uses generateNorthandSouthPoleMaps to generate a map. """

    # Get list of all days / time values to plot that exist in one .nc file
    timeList = printDateTime(output, timeStringVariable=START_TIME_VARIABLE, days=days)

    for i in range(days):
        textBoxString = "Time: " + str(timeList[i])
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)
        variableForOneDay = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, 
                                                                           latCell, lonCell, variableForOneDay, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        artists.append([northPoleScatter, southPoleScatter, textBox])

    if colorBar:
        plt.colorbar(northPoleScatter, ax=northMap)
        plt.colorbar(southPoleScatter, ax=southMap)

    print("Saved .png")
    return artists

def generateArtistsNorth(fig, northMap, latCell, lonCell, output, 
                 mapImageFileName, days, artists, colorbar=True):

    # Get list of all days / time values to plot that exist in one .nc file
    timeList = printDateTime(output, timeStringVariable=START_TIME_VARIABLE, days=days)
    
    for i in range(days):
        textBoxString = "Time: " + str(timeList[i])
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)
        variableForOneDay = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter = generateNorthPoleMap(fig, northMap, 
                                                                           latCell, lonCell, variableForOneDay, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        artists.append([northPoleScatter, textBox])

    if colorbar:
        plt.colorbar(northPoleScatter, ax=northMap)
    
    print("Saved .png")
    return artists

def animateFromMultipleFiles(artists):
    files = gatherFiles()

def main():

    startTime = time.time()

    artists = []
    
    latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, outputFileName)

    ###################
    # NORTH AND SOUTH #
    ###################

    # fig, northMap, southMap = generateNorthandSouthPoleAxes()

    # addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    # addMapFeatures(southMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)

    # artists = generateArtistsNorthAndSouth(fig, northMap, southMap, latCell, lonCell, 
    #                      output, mapImageFileName, days, artists)

    # saveAnimation(fig, artists, animationFileName, startTime)

    ##############
    # NORTH ONLY #
    ##############

    fig, northMap = generateNorthPoleAxes()
    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    artists = generateArtistsNorth(fig, northMap, latCell, lonCell, output, mapImageFileName, days, artists) 
    saveAnimation(fig, artists, animationFileName, startTime)

if __name__ == "__main__":
    main()