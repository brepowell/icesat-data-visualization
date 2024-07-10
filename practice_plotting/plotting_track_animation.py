# Work in progress

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *

def returnCellIndices(output):
    """ Get only the indices that correspond to the E3SM mesh. """
    indices = output.variables["cell"][:1]
    print(indices[0:20])
    return indices.ravel()

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

    indexArray = returnCellIndices(output) # Figure out which cells have data
    print(indexArray[0:10])

    print(ma.min(indexArray))
    print(ma.max(indexArray))

    plt.hist(indexArray, bins=1000)  # arguments are passed to np.histogram
    plt.title("Histogram with 'auto' bins")
    plt.show()

    latCell = latCell[indexArray] # Plot only the cells that have data
    print(latCell[0:10])

    lonCell = lonCell[indexArray] # Plot only the cells that have data
    print(lonCell[0:10])
    variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)

    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    scatterNorth, scatterSouth = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, "sat_track1", 1,1,1,1,1)
    print("Generated .png file")

    ani = animation.FuncAnimation(fig=fig, func=update, frames=100, interval=30)
    ani.save(filename="satellite_track.gif", writer="pillow")
    print("Saved animation as a .gif")

if __name__ == "__main__":
    main()