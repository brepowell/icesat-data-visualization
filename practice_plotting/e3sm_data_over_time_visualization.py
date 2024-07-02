import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *

def main():

    # Load the mesh and data to plot.
    latCell, lonCell    = loadMesh(runDir, meshFileName)
    output              = loadData(runDir, outputFileName)
    days                = getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT)
    artists = []
    mapImageFileName = 'seaice_Output_1.png'

    fig, northMap, southMap = generateNorthandSouthPoleAxes()

    for i in range(days):
        day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, day, mapImageFileName, 1,1,1,1)
        artists.append([northPoleScatter, southPoleScatter])

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=1000)

    plt.colorbar(northPoleScatter, ax=northMap)
    plt.colorbar(southPoleScatter, ax=southMap)

    plt.show()
    ani.save(filename="world.gif", writer="pillow")

if __name__ == "__main__":
    main()