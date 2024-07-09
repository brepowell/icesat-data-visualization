# Work in progress

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *

def main():

    def update(frame):
        # for each frame, update the data stored on each artist.
        x = latCell[:frame]
        y = lonCell[:frame]
        z = variableToPlot1Day[:frame]
        
        # update the scatter plot:
        data = np.stack([x, y, z]).T
        scatterNorth.set_offsets(data)
        scatterSouth.set_offsets(data)
        return (scatterNorth, scatterSouth)

    # Load the mesh and data to plot.
    latCell, lonCell = loadMesh(runDir, meshFileName)
    output = loadData(runDir, outputFileName)

    # printAllAvailableVariables(output)
    variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)
    print(variableToPlot1Day.shape)

    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    scatterNorth, scatterSouth = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, "sat_track1", 1,1,1,1,1)

    # ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
    # plt.show()
    # ani.save(filename="satellite_track.gif", writer="pillow")

if __name__ == "__main__":
    main()