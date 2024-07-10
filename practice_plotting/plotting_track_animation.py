# Work in progress

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *

def returnCellIndices(output):
    """ Get only the indices that correspond to the E3SM mesh. """
    indices = output.variables["cell"][:1]
    return indices.ravel()

def getLatLon(output):
    latCell = output.variables["latitude"][:1]
    latCell = latCell.ravel()
    lonCell = output.variables["longitude"][:1]
    lonCell = lonCell.ravel()
    return latCell, lonCell

def downsample_data(latCell, lonCell, variableToPlot1Day, factor):
    """ Downsample the data arrays by the given factor. """
    latCell_ds = latCell[::factor]
    lonCell_ds = lonCell[::factor]
    variableToPlot1Day_ds = variableToPlot1Day[::factor]
    return latCell_ds, lonCell_ds, variableToPlot1Day_ds

def main():

    def update(frame):
        # Update the data stored on each artist for each frame
        scatterNorth.set_offsets(np.c_[lonCell[:frame], latCell[:frame]])
        scatterSouth.set_offsets(np.c_[lonCell[:frame], latCell[:frame]])
        return scatterNorth, scatterSouth
    
    # Load the data to plot
    output = loadData(runDir, outputFileName)
    latCell, lonCell = getLatLon(output)
    variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)

    # Downsample the data
    factor = 70  # Downsampling factor
    latCell, lonCell, variableToPlot1Day = downsample_data(latCell, lonCell, variableToPlot1Day, factor)

    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    scatterNorth, scatterSouth = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, "sat_track1", 1,1,1,1,1,5.0)
    print("Generated .png file")

    import time
    startTime = time.time()
    ani = animation.FuncAnimation(fig=fig, func=update, frames=latCell.size, interval=1)
    ani.save(filename="satellite_track.gif", writer="pillow")
    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

    # =======================
    print("Saved .gif file")

if __name__ == "__main__":
    main()