# Author:   Breanna Powell
# Date:     07/02/2024

##########
# TO RUN #
##########

# Use the config.py file to specify max latitude, max longitude, file paths, etc.
# Make sure that you navigate to the directory that contains e3sm_data_over_time_visualization.py
# Make sure that the e3sm_data_visualization.py file is also in the same directory.
# Make sure that utility.py is in the same directory

# $ python e3sm_data_over_time_visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from e3sm_data_visualization import *
from utility import *
import time

def saveAnimation(fig, artists, animationFileName, interval=INTERVALS):
    """ Takes in a figure and a list of artists, then it saves those as a .gif. """
    # Debug statements to check the inputs

    print(f"Number of artists: {len(artists)}")
    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=interval)
    ani.save(filename=animationFileName, writer="pillow")
    print("Saved .gif")

def generateArtistsNorthAndSouth(fig, northMap, southMap, latCell, lonCell, output, 
                         mapImageFileName, days, artists, colorbar = True):
    """ For the north and south pole,
    this will make a scatter plot and time stamp per timestep of data in one .nc file.
    Cycle through each day in one output file and map a scatter plot of that full range of days.
    It uses generateNorthandSouthPoleMaps to generate scatterplots to append to a 
    list of artists for the matplotlib Animation package. """

    # Get list of all days / time values to plot that exist in one .nc file
    timeList = printDateTime(output, timeStringVariable=START_TIME_VARIABLE, days=days)

    for i in range(days):
        textBoxString = "Time: " + str(timeList[i])
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)
        variableForOneDay = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter, southPoleScatter = generateNorthandSouthPoleMaps(fig, northMap, southMap, 
                                                                           latCell, lonCell, variableForOneDay, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        artists.append([northPoleScatter, southPoleScatter, textBox])
        print("Day: ", i)

    if colorbar:
        plt.colorbar(northPoleScatter, ax=northMap)
        plt.colorbar(southPoleScatter, ax=southMap)

    print("Saved .png")
    return artists

def generateArtistsNorth(fig, northMap, latCell, lonCell, output, 
                 mapImageFileName, days, artists, colorbar=True):
    """ For the north pole, 
    this will make a scatter plot and time stamp per timestep of data in one .nc file.
    Cycle through each day in one output file and map a scatter plot of that full range of days.
    It uses generateNorthandSouthPoleMaps to generate scatterplots to append to a 
    list of artists for the matplotlib Animation package. """

    #TODO - FIX ANY HARD CODING

    # Get list of all days / time values to plot that exist in one .nc file
    timeString = printDateTime(output)
    
    for i in range(days):
        textBoxString = f"Time: {(SEASON).title()} 200" + str(timeString) # changed from timeList[i]
        textBox = northMap.text(0.05, 0.95, textBoxString, transform=northMap.transAxes, fontsize=14,
                verticalalignment='top', bbox=boxStyling)
        variableForOneDay = reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=i)
        northPoleScatter = generateNorthPoleMap(fig, northMap, 
                                                                           latCell, lonCell, variableForOneDay, 
                                                                           mapImageFileName, 0,0,0,0,0,0)
        print("generated scatter plot", i)
        artists.append([northPoleScatter, textBox])

    if colorbar:
        plt.colorbar(northPoleScatter, ax=northMap)
    
    print("Saved .png")
    return artists

def animateNorthAndSouth(runDir, meshFileName, outputFileName):
    """ Animate the north and south pole, using a certain mesh and .nc output file
     that has daily information for more than one day. """
    
    artists = []    
    latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, outputFileName)

    fig, northMap, southMap = generateNorthandSouthPoleAxes()

    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    addMapFeatures(southMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)

    return fig, generateArtistsNorthAndSouth(fig, northMap, southMap, latCell, lonCell, 
                         output, mapImageFileName, days, artists)

def animateNorth(runDir, meshFileName, outputFileName):
    """ Animate just the north pole, using a certain mesh and .nc output file
     that has daily information for more than one day."""
    
    artists = []
    latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, outputFileName)

    fig, northMap = generateNorthPoleAxes()
    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    return fig, generateArtistsNorth(fig, northMap, latCell, lonCell, output, mapImageFileName, days, artists) 
    
def animateNorthAndSouthFromMultipleFiles():
    """ Reads in a subdirectory of files and maps those on a scatterplot 
    of the north and south poles. Make sure that the subdirectory to the folder containing
    all the data files is specified in the config file. """
    files = gatherFiles(0)

    files = files.sort()
    print("Sorted: ", files)

    artists = []
    fig, northMap, southMap = generateNorthandSouthPoleAxes()
    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    addMapFeatures(southMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    addColorBar = False

    for file in files:
        latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, subdirectory+file)
        
        # This conditional ensures the colorbar is added only once.
        if not addColorBar:
            artists = generateArtistsNorthAndSouth(
                fig, northMap, southMap, latCell, lonCell, output, 
                mapImageFileName, days, artists, colorbar=True)
            
            addColorBar = True
        else:
            artists = generateArtistsNorthAndSouth(
                fig, northMap, southMap, latCell, lonCell, output, 
                mapImageFileName, days, artists, colorbar=False)
            
        print("Length of Artists: ", len(artists))
            
    return fig, artists

def animateNorthFromMultipleFiles():
    """ Reads in a subdirectory of files and maps those on a scatterplot 
    of the north and south poles. Make sure that the subdirectory to the folder containing
    all the data files is specified in the config file. """
    files = gatherFiles(0)
    artists = []

    fig, northMap = generateNorthPoleAxes()
    addMapFeatures(northMap, oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, grid=GRIDON, coastlines=COASTLINES)
    addColorBar = False

    for file in files:
        latCell, lonCell, output, days = loadAllDays(runDir, meshFileName, subdirectory+file)
        
        # This conditional ensures the colorbar is added only once.
        if not addColorBar:
            artists = generateArtistsNorth(
                fig, northMap, latCell, lonCell, output, 
                mapImageFileName, days, artists, colorbar=True)
            
            addColorBar = True
        else:
            artists = generateArtistsNorth(
                fig, northMap, latCell, lonCell, output, 
                mapImageFileName, days, artists, colorbar=False)
            
    return fig, artists

def main():

    startTime = time.time()
    #fig, artists = animateNorthAndSouth(runDir, meshFileName, outputFileName)
    fig, artists = animateNorthAndSouthFromMultipleFiles()
    #fig, artists = animateNorthFromMultipleFiles()
    saveAnimation(fig, artists, animationFileName)
    endTime = time.time()
    print("It took this much time: ", endTime-startTime)

if __name__ == "__main__":
    main()