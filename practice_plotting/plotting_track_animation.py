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
import time
from datetime import datetime, timedelta 
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

def printDateTime(output):
    """ Prints and returns the date from the .nc file's time_string variable. """
    rawTime = output.variables["time_string"][:1].ravel()
    timeString = "time_stamp decoded: "
    for i in range(len(rawTime)):
        timeString += rawTime[i].decode()
    print(timeString)
    return timeString 

def convertTime(start):
    base_date = datetime(2000, 1, 1)
    d = base_date + timedelta(hours=start)
    timeString = d.strftime("%Y-%m-%d %H:%M:%S")
    print("Time converted", timeString)
    return timeString

def getTime(output, length):
    """ Pull the timestamp from the .nc file. Populate an array with times. """
    start = float(output.variables["time"][:1])
    stop = output.variables["time"][:1] + length
    step = .00036 # How much time elapses between pulses (there are 10,000 pulses per second)
    return np.arange(start, stop, step)
    
def downsampleData(latCell, lonCell, timeCell, variableToPlot1Day, factor):
    """ Downsample the data arrays by the given factor. """
    return latCell[::factor], lonCell[::factor], timeCell[::factor], variableToPlot1Day[::factor]

def plotNorthAndSouthTrackAnimation():
    
    # Load the data to plot
    output              = loadData(runDir, outputFileName)
    latCell, lonCell    = getLatLon(output)
    timeCell            = getTime(output, len(lonCell))

    variableToPlot1Day  = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT)

    # Downsample the data
    factor = 100  # Downsampling factor
    latCell, lonCell, timeCell, variableToPlot1Day = downsampleData(latCell, lonCell, timeCell, variableToPlot1Day, factor)

    # Plot the north and south poles
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    scatterNorth, scatterSouth = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, 1,1,1,1,1,5.0)
    
    # Initialize the text box
    textBox = northMap.text(0.05, 0.95, "", transform=northMap.transAxes, fontsize=14, verticalalignment='top', bbox=boxStyling)

    def update(frame):
        # Update the data stored on each artist for each frame
        scatterNorth.set_offsets(np.c_[lonCell[:frame], latCell[:frame]])
        scatterSouth.set_offsets(np.c_[lonCell[:frame], latCell[:frame]])

        # Update the text box with the current time
        textBoxString = "Time: " + str(convertTime(timeCell[frame]))
        textBox.set_text(textBoxString)

        return scatterNorth, scatterSouth, textBox

    print("Generated .png file")

    startTime = time.time()
    ani = animation.FuncAnimation(fig=fig, func=update, frames=latCell.size, interval=1)
    ani.save(filename=animationFileName, writer="pillow")
    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

    # =======================
    print("Saved .gif file")

def plotNorthPoleTrackAnimation():
    
    # Load the data to plot
    output              = loadData(runDir, outputFileName)
    latCell, lonCell    = getLatLon(output)
    timeCell            = getTime(output, len(lonCell))

    variableToPlot1Day  = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT)

    # Downsample the data
    factor = 100  # Downsampling factor
    latCell, lonCell, timeCell, variableToPlot1Day = downsampleData(latCell, lonCell, timeCell, variableToPlot1Day, factor)

    # Plot the north pole
    fig, northMap = generateNorthPoleAxes()
    scatterNorth = generateNorthPoleMap(fig, northMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, 1,1,1,1,1,5.0)
    
    # Initialize the text box
    textBox = northMap.text(0.05, 0.95, "", transform=northMap.transAxes, fontsize=14, verticalalignment='top', bbox=boxStyling)

    def update(frame):
        # Update the data stored on each artist for each frame
        scatterNorth.set_offsets(np.c_[lonCell[:frame], latCell[:frame]])

        # Update the text box with the current time
        textBoxString = "Time: " + str(convertTime(timeCell[frame]))
        textBox.set_text(textBoxString)

        return scatterNorth, textBox

    print("Generated .png file")

    startTime = time.time()
    ani = animation.FuncAnimation(fig=fig, func=update, frames=latCell.size, interval=1)
    ani.save(filename=animationFileName, writer="pillow")
    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

    # =======================
    print("Saved .gif file")


def main():
    # plotNorthAndSouthTrackAnimation()
    plotNorthPoleTrackAnimation()

if __name__ == "__main__":
    main()