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

def loadAllDays(runDir, meshFileName, outputFileName):
    # Load the mesh and data to plot.
    latCell, lonCell    = loadMesh(runDir, meshFileName)
    output              = loadData(runDir, outputFileName)
    days                = getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT)

    return latCell, lonCell, output, days

def animateNorthAndSouth(fileName, runDir, meshFileName, outputFileName):

    latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, outputFileName)
    artists = []

    startTime = time.time()

    fig, northMap, southMap = generateNorthandSouthPoleAxes()

    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    addMapFeatures(southMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
        
    for i in range(days):
        textBoxString = "Day: " + str(i+1)
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)
        variableForOneDay = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, 
                                                                           latCell, lonCell, variableForOneDay, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        artists.append([northPoleScatter, southPoleScatter, textBox])

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=1000)

    plt.colorbar(northPoleScatter, ax=northMap)
    plt.colorbar(southPoleScatter, ax=southMap)

    print("Saved .png")
    ani.save(filename=fileName, writer="pillow")
    print("Saved .gif")

    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

def animateNorth(fileName, runDir, meshFileName, outputFileName):

    latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, outputFileName)
    artists = []

    startTime = time.time()

    fig, northMap = generateNorthPoleAxes()

    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)

    for i in range(days):
        textBoxString = "Day: " + str(i+1)
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)
        variableForOneDay = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter = generateNorthPoleMap(fig, northMap, 
                                                                           latCell, lonCell, variableForOneDay, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        artists.append([northPoleScatter, textBox])

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=1000)

    plt.colorbar(northPoleScatter, ax=northMap)

    print("Saved .png")
    ani.save(filename=fileName, writer="pillow")
    print("Saved .gif")

    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

def animateFromMultipleFiles():
    files = gatherFiles()

def main():

    latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, outputFileName)
    timeString = printDateTime(output, timeStringVariable="xtime_startDaily", days=5)

    # Change file name in config file
    #animateNorthAndSouth(animationFileName, runDir, meshFileName, outputFileName) 
    #animateNorth(animationFileName, runDir, meshFileName, outputFileName) 

if __name__ == "__main__":
    main()