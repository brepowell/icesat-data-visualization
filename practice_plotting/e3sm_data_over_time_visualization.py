# Author:   Breanna Powell
# Date:     07/02/2024

##########
# TO RUN #
##########

# Use the config.py file to specify max latitude, max longitude, file paths, etc.
# Make sure that you navigate to the directory that contains e3sm_data_over_time_visualization.py
# Make sure that the e3sm_data_practice_visualization.py file is also in the same directory.

# $ python e3sm_data_over_time_visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from e3sm_data_practice_visualization import *
from config import *
import time

def createGIFAnimation(fileName, runDir, meshFileName, outputFileName):

    # Load the mesh and data to plot.
    latCell, lonCell    = loadMesh(runDir, meshFileName)
    output              = loadData(runDir, outputFileName)
    days                = getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT)
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

def main():

    # Change file name in config file
    createGIFAnimation(animationFileName, runDir, meshFileName, outputFileName) 

if __name__ == "__main__":
    main()