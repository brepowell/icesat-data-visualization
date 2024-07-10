# Work in progress

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *

def returnCellIndices(output):
    """ Get only the indices that correspond to the E3SM mesh. """
    indices = output.variables["cell"][:1]
    return indices.ravel()

def main():

    def update(frame):
        # for each frame, update the data stored on each artist.
        x = lonCell[:frame]
        y = latCell[:frame]
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
    latCell = latCell[indexArray] # Plot only the cells that have data
    lonCell = lonCell[indexArray] # Plot only the cells that have data
    variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)

    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    scatterNorth, scatterSouth = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, "sat_track1", 1,1,1,1,1)
    print("Generated .png file")

    ani = animation.FuncAnimation(fig=fig, func=update, frames=latCell.size)
    ani.save(filename="satellite_track.gif", writer="pillow")
    print("Saved animation as a .gif")

if __name__ == "__main__":
    main()