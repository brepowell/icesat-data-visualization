# Author:   Breanna Powell
# Date:     07/10/2024

##########
# TO RUN #
##########

# Use the config.py file to specify file paths, etc.
# Make sure that you navigate to the directory that contains plotting_track_animation.py
# Have a folder labeled "satellite_data_preprocessed" in that directory
# The data folder must contain the output file
# Make sure that the e3sm_data_practice_visualization.py file is also in the same directory.

# $ python plotting_track_animation.py

import numpy as np
import matplotlib.animation as animation
from e3sm_data_practice_visualization import *

def returnCellIndices(output):
    """ Get only the indices that correspond to the E3SM mesh. """
    indices = output.variables["cell"][:1]
    return indices.ravel()

def getLatLon(output):
    """ Pull the latitude and longitude variables from an .nc file. """
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
    variableToPlot1Day = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT)

    # Downsample the data
    factor = 100  # Downsampling factor
    latCell, lonCell, variableToPlot1Day = downsample_data(latCell, lonCell, variableToPlot1Day, factor)

    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    scatterNorth, scatterSouth = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, 1,1,1,1,1,5.0)
    print("Generated .png file")

    import time
    startTime = time.time()
    ani = animation.FuncAnimation(fig=fig, func=update, frames=latCell.size, interval=1)
    ani.save(filename=animationFileName, writer="pillow")
    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

    # =======================
    print("Saved .gif file")

if __name__ == "__main__":
    main()