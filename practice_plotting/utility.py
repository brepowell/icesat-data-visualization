# Utility functions needed for .nc files
from config import *
import netCDF4                      # For opening .nc files for numpy
import numpy as np
from datetime import datetime, timedelta 
import time
import matplotlib as mpl

def loadMesh(runDir, meshFileName):
    """ Load the mesh from an .nc file. 
    The mesh must have the same resolution as the output file. """
    print('read: ', runDir, meshFileName)

    dataset = netCDF4.Dataset(runDir + meshFileName)
    latCell = np.degrees(dataset.variables['latCell'][:]) # Convert from radians to degrees.
    lonCell = np.degrees(dataset.variables['lonCell'][:]) # Convert from radians to degrees.

    return latCell, lonCell

def loadData(runDir, outputFileName):
    """ Load the data from an .nc output file. 
    Returns a 1D array of the variable you want to plot of size nCells.
    The indices of the 1D array match with those of the latitude and longitude arrays, 
    which are also size nCells."""
    print('read: ', runDir, outputFileName)

    return netCDF4.Dataset(runDir + outputFileName)

def printAllAvailableVariables(output):
    """ See what variables you can use in this netCDF file. 
    Requires having loaded a netCDF file into an output variable. 
    This is an alternative to the ncdump command. 
    It's useful because it displays the shape of each variable as well."""
    print(output.variables) # See all variables available in the netCDF file

def getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT):
    """ Find out how many days are in the simulation by looking at the netCDF file 
    and at the variable you have chosen to plot. """
    variableForAllDays = output.variables[keyVariableToPlot][:]
    return variableForAllDays.shape[0]

def loadAllDays(runDir, meshFileName, outputFileName):
    """ Load the mesh and data to plot. """
    latCell, lonCell    = loadMesh(runDir, meshFileName)
    output              = loadData(runDir, outputFileName)
    days                = getNumberOfDays(output, keyVariableToPlot=VARIABLETOPLOT)

    return latCell, lonCell, output, days

def reduceToOneDay(output, keyVariableToPlot=VARIABLETOPLOT, dayNumber=0):
    """ Reduce the variable to one day's worth of data so we can plot 
    using each index per cell. The indices for each cell of the 
    variableToPlot1Day array coincide with the indices 
    of the latCell and lonCell. """
    
    variableForAllDays = output.variables[keyVariableToPlot][:]
    variableToPlot1Day = variableForAllDays[dayNumber,:]                                     
    # print("variableToPlot1Day", variableToPlot1Day[0:5])

    return variableToPlot1Day

def gatherFiles(fullPath = True):
    """ Use the subdirectory specified in the config file. 
    Get all files in that folder. """
    filesToPlot = []
    print("Full path is ", FULL_PATH)

    if fullPath:
        for root, dirs, files in os.walk(FULL_PATH, topdown=False):
            for name in files:
                if name.endswith('.nc'):
                    filesToPlot.append(os.path.join(root, name))

    else:
        for root, dirs, files in os.walk(FULL_PATH, topdown=False):
            for name in files:
                if name.endswith('.nc'):
                    filesToPlot.append(name)

    print("Read this many files: ", len(filesToPlot))

    return filesToPlot

def downsampleData(latCell, lonCell, timeCell, variableToPlot1Day, factor=DEFAULT_DOWNSAMPLE_FACTOR):
    """ Downsample the data arrays by the given factor. """
    return latCell[::factor], lonCell[::factor], timeCell[::factor], variableToPlot1Day[::factor]

def downsampleData(variable, factor=DEFAULT_DOWNSAMPLE_FACTOR):
    """ Downsample the data arrays by the given factor. """
    return variable[::factor]

def returnCellIndices(output):
    """ Get only the indices that correspond to the E3SM mesh. """
    indices = output.variables[CELLVARIABLE][:1]
    return indices.ravel()

def getLatLon(output):
    """ Pull the latitude and longitude variables from an .nc file. """
    latCell = output.variables[LATITUDEVARIABLE][:1]
    latCell = latCell.ravel()
    lonCell = output.variables[LONGITUDEVARIABLE][:1]
    lonCell = lonCell.ravel()
    return latCell, lonCell

def printDateTime(output, timeStringVariable = TIMESTRINGVARIABLE, days = 1):
    """ Prints and returns the date from the .nc file's time string variable. 
    This assumes that the time needs to be decoded and is the format
    [b'0' b'0' b'0' b'1' b'-' b'0' b'1' b'-' b'0' b'2' b'_' b'0' b'0' b':' b'0' b'0' b':' b'0' b'0']
    """

    # Get all the time variables
    rawTime = output.variables[timeStringVariable][:days]
    rawTime = rawTime.ravel()
    rawTime = bytearray(rawTime).decode()
    timeStrings = rawTime.split('\x00')
    timeStrings[:] = [x for x in timeStrings if x]
    
    if len(timeStrings) == 1:
        print(timeStrings[0])
        return timeStrings[0]
    
    print(timeStrings)
    return timeStrings

def convertTime(timeToConvert):
    """ Convert time from proleptic_gregorian to a human-readable string."""
    base_date = datetime(2000, 1, 1)
    d = base_date + timedelta(hours=timeToConvert)
    timeString = d.strftime("%Y-%m-%d %H:%M:%S")
    print("Time converted", timeString)
    return timeString

def getTimeArrayFromStartTime(output, length):
    """ Pull the starting timestamp from the .nc file. 
    Populate an array with times. (These are approximate, not real)"""
    start = float(output.variables["time"][:1])
    stop = output.variables[TIMEVARIABLE][:1] + length
    step = .00036 # How much time elapses between pulses (there are 10,000 pulses per second)
    return np.arange(start, stop, step)