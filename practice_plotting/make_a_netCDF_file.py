# Breanna Powell
# Created: 07/17/2024

# See this great tutorial about writing netCDF files:
# https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing/

import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import os
from utility import *

import glob
from pathlib import Path

USER                = os. getlogin()                        #TODO: check if this is ok for Perlmutter
SOURCE              = "SOME PATH NAME TO FILL IN LATER"     #TODO: make this dynamic

FILL_VALUE      = -99999.0

DENSITY_WATER   = 1026
DENSITY_ICE     = 917
DENSITY_SNOW    = 330

    #Clusters  1        2         3       4
SEASONS = ["spring", "summer", "fall", "winter"]

def loadSynchronizer(synchronizerFile=SYNCH_FILE_NAME):
    """ Loads the synchronizer file that is organized in chronological order.
    Returns arrays of the time details for each satellite track and the total number of files. """
    synchData        = loadData(runDir, synchronizerFile) # Make sure that runDir is set to perlmutterpath1
    shapeOfSynchData = synchData.variables["time_string"].shape
    timeStrings  = printDateTime(synchData, "time_string", shapeOfSynchData[0])

    # For ALL satellite data files:
    timeCluster     = synchData.variables["seasonalcluster"]
    timeYear        = synchData.variables["year"]
    timeMonth       = synchData.variables["month"]
    timeDay         = synchData.variables["day"]
    timeHour        = synchData.variables["hour"]
    timeGregorian   = synchData.variables["time"]

    print("===== SYNCH FILE DETAILS ======")
    # Looking at one specific satellite file
    fileCount = shapeOfSynchData[0]

    return fileCount, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian

def getFileIndicesFromSynchronizerBySeasonalCluster(timeClusters):
    """ Look at the seasonal cluster array from the synch file. Return the indices for the
    season in specified in the config.py file. """
    print("Season is ", SEASON)
    season = SEASONS.index(SEASON) + 1  # Seasons are 1, 2, 3, 4
    return [i for i in range(len(timeClusters)) if timeClusters[i] == season]

def getFileIndicesFromSynchronizerByYear(timeYears):
    """ Look at the year array from the synch file. Return the indices for the
    year in specified in the config.py file. """
    print("Year is ", YEAR)
    return [i for i in range(len(timeYears)) if timeYears[i] == int(YEAR)]

# From https://www.geeksforgeeks.org/python-intersection-two-lists/#
def intersection(lst1, lst2):
    """ Return the intersection of two lists (what they have in common)."""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

#TODO: Make sure the data types are correct; there should be an "f" after many of them (from Andrew's example file)
def createVariableForNetCDF(ncfile, shortName, longName, vmax, vmin = 0.0, fillvalue = None, dtype = np.float64):
    """ Add a variable to the netCDF file. 
    It will appear in the header info. """
    variable = ncfile.createVariable(shortName, dtype, ('nCells',))
    variable.long_name = longName
    variable.valid_range = (vmin, vmax)
    if fillvalue != None:
        variable._fillvalue = fillvalue
    return variable

def printSatelliteTimeDetails(fileIndex, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian):
    """ Take in arrays of time details and a fileIndex. Print and return those details
    for a specific satellite file. This assumes the synch file was read and that the
    time details have been filled in with values from the synch file. """
    print("File index is    ", fileIndex)
    
    timeString  = timeStrings[fileIndex]
    cluster     = timeCluster[fileIndex]
    year        = timeYear[fileIndex]
    month       = timeMonth[fileIndex]
    day         = timeDay[fileIndex]
    hour        = timeHour[fileIndex]
    gregorian   = timeGregorian[fileIndex]

    print("Time String:     ", timeString)
    print("Cluster:         ", cluster)
    print("Year:            ", year)
    print("Month:           ", month)
    print("Day:             ", day)
    print("Hour:            ", hour)
    print("Gregorian Time:  ", gregorian)

    return timeString, cluster, year, month, day, hour, gregorian

# Not used currently
def returnListOfSatFileNamesBySeasonAndYear(season = "*", year = "*"):
    """ Assumes that the synch file was read and that arrays have been filled
    with the time information for all satellite files. This can be used to return a list of files that match a pattern. Uses glob for this. """

    filenamePattern = f"icesat_E3SM_{season}_{year}_*.nc"   

    searchPattern = os.path.join(perlmutterpathSatellites, filenamePattern)
    matchingFiles = glob.glob(searchPattern)
    return matchingFiles

def loadOneSatFile(fileIndex, previousday, dayCount, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian):
    """ Assumes that the synch file was read and that arrays have been filled
    with the time information. """

    timeString, cluster, year, month, day, hour, gregorian = printSatelliteTimeDetails(fileIndex, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian)

    if previousday != day:
        dayCount += 1
    previousday = day

    #satelliteFileName   = r"\satellite_data_preprocessed\one_day\icesat_E3SM_spring_2008_02_22_16.nc"
    #satelliteFileName    = r"icesat_E3SM_spring_2008_02_22_16.nc" #PM

    # ALL SATELLITE FILES - Find the file using the file name pattern
    filenamePattern = f"icesat_E3SM_*_{year}_{str(month).zfill(2)}_{str(day).zfill(2)}_{str(hour).zfill(2)}.nc"
    
    searchPattern = os.path.join(perlmutterpathSatellites, filenamePattern)
    matchingFiles = glob.glob(searchPattern)
    satelliteFileName = matchingFiles[0] if matchingFiles else None
    print("Matching files: ", matchingFiles)
    print("Satellite file name: ", satelliteFileName)
    return satelliteFileName, previousday, dayCount

def getThickness(gridCellAveragedThickness, iceConcentration):
    """ Grid cell averaged thickness is the same as the sea ice volume variable in E3SM.
    Concentration is the same as the sea ice area variable in E3SM.
    volume / area of cell = height (thickness) 
    """
    return gridCellAveragedThickness / iceConcentration

def getFreeboard(heightIce, heightSnow):
    """Formula to calculate freeboard: hf = hi (pw-pi)/pw + hs (pw-ps)/pw.
    Where p means density; h is height, w is water, i is ice, s is snow"""
    return heightIce*(DENSITY_WATER-DENSITY_ICE)/DENSITY_WATER + heightSnow*(DENSITY_WATER-DENSITY_SNOW)/DENSITY_WATER

def main():
    
    ##################################
    # OPEN THE MESH & SET CELL COUNT #
    ##################################
    latCell, lonCell = loadMesh("", meshFileName) # Make sure that runDir is set to perlmutterpath1
    print("nCells", latCell.shape[0])
    CELLCOUNT = latCell.shape[0]

    ########################
    # Use the synchronizer #
    ########################
    fileCount, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian = loadSynchronizer()
    print("Number of satellite tracks in Synch file: ", fileCount)

    # Get all file indices by season and by year; find the intersection of those lists
    seasonFileIndices = getFileIndicesFromSynchronizerBySeasonalCluster(np.array(timeCluster))
    yearFileIndices = getFileIndicesFromSynchronizerByYear(np.array(timeYear))
    fileIndices = intersection(seasonFileIndices, yearFileIndices)
    print(f"File indices for {SEASON} {YEAR}: ", fileIndices)

    ########################
    # OPEN THE NETCDF FILE #
    ########################

    try: ncfile.close()  # just to be safe, make sure dataset is not already open.
    except: pass
    ncfile = Dataset(NEW_NETCDF_FILE_NAME, mode='w', format='NETCDF4_CLASSIC') 

    ##############
    # DIMENSIONS #
    ##############

    # Create the dimensions (nCells is the only dimension needed)
    nCells = ncfile.createDimension('nCells', CELLCOUNT)

    ##############
    # ATTRIBUTES #
    ##############

    # Grab the date for the header information
    now = datetime.now()
    historyString = now.strftime("%d-%B-%Y %H:%M:%S") + ": File created by " + USER

    # Set the attributes
    ncfile.title        = "Comparison of icesat freeboard with E3SM"
    ncfile.source       = SOURCE
    ncfile.history      = historyString
    ncfile.institution  = "Los Alamos National Laboratory"

    #############
    # VARIABLES #
    #############

    effmf   = createVariableForNetCDF(ncfile, "effmf", "model freeboard effective sample size", 
                            vmax = 29.88248, fillvalue = FILL_VALUE)
    effof   = createVariableForNetCDF(ncfile, "effof", "observed freeboard effective sample size", 
                            vmax = 22321.38, vmin = 0.2787585, fillvalue = FILL_VALUE)
    meanmf  = createVariableForNetCDF(ncfile, "meanmf", "model freeboard mean", 
                            vmax = 0.9041953, vmin = 0.01583931, fillvalue = FILL_VALUE)
    meanof  = createVariableForNetCDF(ncfile, "meanof", "observed freeboard mean", 
                            vmax = 1.14699, fillvalue = FILL_VALUE)
    samplemf = createVariableForNetCDF(ncfile, "samplemf", "model freeboard sample count", 
                            vmax = 296)
    sampleof = createVariableForNetCDF(ncfile, "sampleof", "observed freeboard sample count", 
                            vmax = 46893)
    stdmf   = createVariableForNetCDF(ncfile, "stdmf", "model freeboard standard deviation", 
                            vmax = 0.2506092, vmin = 0.005416268, fillvalue = FILL_VALUE)
    stdof   = createVariableForNetCDF(ncfile, "stdof", "observed freeboard standard deviation", 
                            vmax = 0.9629242, vmin = 0.01656876, fillvalue = FILL_VALUE)

    ###################
    # SATELLITE FILES #
    ###################

    samples      = np.zeros(CELLCOUNT)
    observations = np.zeros(CELLCOUNT)
    allFreeboardFromSatelliteData = np.zeros((fileCount, CELLCOUNT)) 
    
    dayCount = 1
    previousday = timeDay[0]

    print("Shape of allFreeboardFromSatelliteData:   ", allFreeboardFromSatelliteData.shape)

    for fileIndex in fileIndices:

        satelliteFileName, previousday, dayCount = loadOneSatFile(fileIndex, previousday, dayCount, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian)

        # Load the data from the satellite
        #satelliteData       = loadData(runDir, satelliteFileName) #local
        satelliteData       = loadData("", satelliteFileName) #PM
        
        # Grab the variables from the satellite data file
        freeBoardReadings               = reduceToOneDay(satelliteData, "freeboard")
        cellIndicesForAllSamples        = returnCellIndices(satelliteData, "modcell")
        cellIndicesForAllObservations   = returnCellIndices(satelliteData, "cell")

        # Account for off-by-one converstion from MATLAB to Python indexing
        cellIndicesForAllSamples = cellIndicesForAllSamples - 1
        cellIndicesForAllObservations = cellIndicesForAllObservations - 1

        # Debugging and checking what cells have samples
        # for index in cellIndicesForAllSamples:
        #     samples[index] = 1

        # for index in cellIndicesForAllObservations:
        #     observations[index] = 1

        print("Shape of freeBoardReadings:             ", freeBoardReadings.shape)
        print("Shape of cellIndicesForAllSamples:      ", cellIndicesForAllSamples.shape)
        print("Shape of cellIndicesForAllObservations: ", cellIndicesForAllObservations.shape)

        ############################
        # SATELLITE-ONLY VARIABLES #
        ############################
        # These variables are easy to pull directly from the satellite data.

        # Sample model freeboard is the # of times that cell was passed over 
        # (ex. once in a day) in the full time
        samples += np.bincount(cellIndicesForAllSamples, minlength=CELLCOUNT) # Collect one count of the satellite passing overhead.

        # Sample observation freeboard is the # of photon reads per cell over full time
        observations += np.bincount(cellIndicesForAllObservations, minlength=CELLCOUNT) # Collect all photon counts into bins using cell indices.

        # Collecting all freeboard readings into a matrix for caculating the mean and standard deviation
        allFreeboardFromSatelliteData[fileIndex][cellIndicesForAllObservations] = freeBoardReadings[:]

        # for debugging - checking the latitudes and longitudes indexed
        # satLat = np.array(latCell[cellIndicesForAllSamples])
        # print("Length of latCell", len(latCell))
        # print("Latitude: ", satLat)
        # satLon = np.array(lonCell[cellIndicesForAllSamples])
        # print("Length of lonCell", len(lonCell))
        # print("Longitude: ", satLon)

    print("=== FINISHED GRABBING SATELLITE DATA === ")

    samplemf[:] = samples
    sampleof[:] = observations

    print("===   CALCULATING MEANOF AND STDOF   === ")
    means = np.mean(allFreeboardFromSatelliteData, axis=0, dtype='float')
    stdDeviations = np.std(allFreeboardFromSatelliteData, axis=0, dtype='float')

    # Observed freeboard mean is the sum of all photon readings per cell over time
    # divided by the number of tracks (ex. 409 for spring 2003)
    meanof[:] = means
    stdof[:] = stdDeviations

    print("Number of days", dayCount)

    # # Read data back from variable, print min and max
    print("===== SATELLITE VARIABLES ======")
    print("Shape of samplemf", samplemf[:].shape)
    print("Shape of sampleof", sampleof[:].shape)
    print("Samplemf Min/Max values:", samplemf[:].min(), samplemf[:].max())
    print("Sampleof Min/Max values:", sampleof[:].min(), sampleof[:].max())
    print("Meanof   Min/Max values:", meanof[:].min(),   meanof[:].max())
    print("Stdof    Min/Max values:", stdof[:].min(),    stdof[:].max())

    # ######################################
    # # CALCULATE FREEBOARD FROM THE MODEL #
    # ######################################

    months = np.array(timeMonth[fileIndices])
    months = np.unique(months) # Removing duplicate months
    print(months)

    days = np.array(timeDay[fileIndices])

    # https://stackoverflow.com/questions/32471310/python-split-list-in-subsets-if-the-current-element-is-minor-than-previous-elem
    daysList = []
    prev = float('inf')
    for x in days:
        if x < prev:
            temp = []
            daysList.append(temp)
        temp.append(x)
        prev = x

    print(daysList)

    for row in daysList:
        daysList[row] = np.array(daysList[row])
        daysList[row] = np.unique(daysList[row])

    print(daysList)
    print("Shape of daysList: ", daysList.shape)

    # #modelDailyDataFile  = r"\output_files\Breanna_D_test_1x05_days.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"
    # #modelDailyDataFile  = r"v3.LR.historical_0051.mpassi.hist.am.timeSeriesStatsDaily.2008-02-01.nc" #PM
    # modelDailyDataFile = "v3.LR.historical_0051.mpassi.hist.am.timeSeriesStatsDaily." + str(year) + "-" + str(month).zfill(2) + "-"+ str(1).zfill(2) + ".nc"

    # #modelData           = loadData(runDir, modelDailyDataFile)
    # modelData           = loadData(perlmutterpathDailyData, modelDailyDataFile) #PM
    # snowVolumeCells     = reduceToOneDay(modelData, keyVariableToPlot = "timeDaily_avg_snowVolumeCell", dayNumber = day+1) 
    # iceVolumeCells      = reduceToOneDay(modelData, keyVariableToPlot = "timeDaily_avg_iceVolumeCell", dayNumber = day+1)
    # iceAreaCells        = reduceToOneDay(modelData, keyVariableToPlot = "timeDaily_avg_iceAreaCell", dayNumber = day+1)

    # # Model freeboard mean is 
    # # Model freeboard standard deviation is
    # # Model freeboard effective sample size is
    # # Observation freeboard effective sample size is

    # startTime = modelData.variables[START_TIME_VARIABLE]
    # print("Days in that month:         ", startTime.shape[0])

    # modelTime     = reduceToOneDay(modelData, keyVariableToPlot = START_TIME_VARIABLE, dayNumber = day+1)
    # convertDateBytesToString(modelTime)

    # print("Snow Volume Cells shape:    ", snowVolumeCells.shape)
    # print("Ice Volume Cells shape:     ", iceVolumeCells.shape)
    # print("Ice Area Cells shape:       ", iceAreaCells.shape)

    # # TODO: Future work could be to add the Freeboard variable to E3SM's variables

    # # Freeboard = Sea Ice Thickness * (1 - Sea Ice Density / Seawater Density) + Snow Thickness (1 - Snow Density / Seawater Density)
    # heightIceCells  = getThickness(iceVolumeCells, iceAreaCells)
    # heightSnowCells = getThickness(snowVolumeCells, iceAreaCells)
    # print("Ice Height Cells shape:     ",   heightIceCells.shape)
    # print("Snow Height Cells shape:    ",  heightSnowCells.shape)

    # # height ice + height snow = height water + height of freeboard
    # # freeboard = ice thickness + snow height - water height (which is 0?)
    # all_E3SM_freeboard = getFreeboard(heightIceCells, heightSnowCells)
    # print("E3SM Freeboard - all cells: ", all_E3SM_freeboard.shape)

    # meanmf[:] = all_E3SM_freeboard

    # #Use cellIndicesForAllSamples
    # #Use cellIndicesForAllObservations

    # print("\n=====   MODEL VARIABLES   ======")
    # print("Meanmf   Min/Max values:", meanmf[:].min(),   meanmf[:].max())

    # print("\n=====   ALONG TRACK   ======")
    # freeBoardAlongSatelliteTracks = all_E3SM_freeboard[cellIndicesForAllSamples]
    # print("Shape of freeBoardAlongSatelliteTracks: ", freeBoardAlongSatelliteTracks.shape)
    # print("E3SM Freeboard - along satellite track", freeBoardAlongSatelliteTracks)

    # close the Dataset
    ncfile.close()
    print('Dataset is closed!')

if __name__ == "__main__":
    main()
