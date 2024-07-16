# Author:   Breanna Powell
# Date:     07/10/2024

##########
# TO RUN #
##########

# Use the config.py file to specify file paths, etc.
# Make sure that you navigate to the directory that contains plotting_track_animation.py
# Make sure that the e3sm_data_visualization.py file is also in the same directory.
# Make sure that utility.py is in the same directory.

# $ python plotting_track_animation.py

import matplotlib.animation as animation
from e3sm_data_visualization import *
from utility import *

def plotNorthAndSouthTrackAnimation():
    
    # Load the data to plot
    output              = loadData(runDir, outputFileName)
    latCell, lonCell    = getLatLon(output)
    timeCell            = getTimeArrayFromStartTime(output, len(lonCell))

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
    timeCell            = getTimeArrayFromStartTime(output, len(lonCell))

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