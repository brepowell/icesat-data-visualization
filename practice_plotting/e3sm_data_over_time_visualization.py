# Author:   Breanna Powell
# Date:     07/02/2024

##########
# TO RUN #
##########

# Use the config.py file to specify max latitude, max longitude, file paths, etc.
# Make sure that you navigate to the directory that contains e3sm_data_over_time_visualization.py
# Have a folder labeled "netCDF_files" in that directory
# The data folder must contain the mesh file and the output file
# Make sure that the e3sm_data_practice_visualization.py file is also in the same directory.

# $ python e3sm_data_over_time_visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from e3sm_data_practice_visualization import *
from config import *

def createGIFAnimation(fileName, runDir, meshFileName, outputFileName):

    # Load the mesh and data to plot.
    latCell, lonCell    = loadMesh(runDir, meshFileName)
    output              = loadData(runDir, outputFileName)
    days                = getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT)
    artists = []
    mapImageFileName = 'seaice_both_poles.png'

    fig, northMap, southMap = generateNorthandSouthPoleAxes()

    for i in range(days):
        day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, day, mapImageFileName, 0,1,1,1,1)
        artists.append([northPoleScatter, southPoleScatter])

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=1000)

    plt.colorbar(northPoleScatter, ax=northMap)
    plt.colorbar(southPoleScatter, ax=southMap)

    plt.show()
    ani.save(filename=fileName, writer="pillow")

def main():

    createGIFAnimation("5_day_simulation.gif", runDir, meshFileName, outputFileName) # Just for a 5-day simulation
    # createGIFAnimation("10_day_simulation.gif", runDir, meshFileName, outputFileName)
    # createGIFAnimation("365_day_simulation.gif", runDir, meshFileName, outputFileName)

if __name__ == "__main__":
    main()