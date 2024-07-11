# Work in progress

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *
from plotting_track_animation import *

import os
import netCDF4

path = runDir + subdirectory

def gatherFiles():
    """ Use the subdirectory specified in the config file. Get all files in that folder. """
    
    filesToPlot = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filesToPlot.append(os.path.join(root, name))

    return filesToPlot

def animateTrackLines(filePaths):
    """ Animates all tracks for a given period of time. Depends on what items are
     in the specified subdirectory. """
    
    artists = []
    previousTracks = []  # List to keep track of all artists
    fig, northMap, southMap = generateNorthandSouthPoleAxes()

    # Load the mesh and data to plot.
    for file in filePaths:
        output = netCDF4.Dataset(file)
        latCell, lonCell = getLatLon(output)
        satelliteTrack = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0)
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, latCell, lonCell, satelliteTrack, mapImageFileName, 0,1,1,1,1)
        
        # Allows it to remember all the tracks (not overwrite with each new track)
        previousTracks.extend([northPoleScatter, southPoleScatter])
        artists.append(list(previousTracks)) 

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=100)

    plt.colorbar(northPoleScatter, ax=northMap)
    plt.colorbar(southPoleScatter, ax=southMap)

    ani.save(filename=animationFileName, writer="pillow")
    print("Saved .gif file")

def main():
    filePaths = gatherFiles()
    animateTrackLines(filePaths)

if __name__ == "__main__":
    main()