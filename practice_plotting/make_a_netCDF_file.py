# Breanna Powell
# Created: 07/17/2024

# This is a great tutorial about writing netCDF files:
# https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing/

import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import os
from utility import *

USER        = os. getlogin()                        #TODO: check if this is ok
SOURCE      = "SOME PATH NAME TO FILL IN LATER"     #TODO: make this dynamic
CELLCOUNT   = 233365 #235160

#TODO: Make sure the data types are correct; there should be an "f" after many of them.

try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset('new.nc',mode='w',format='NETCDF4_CLASSIC') 

##############
# DIMENSIONS #
##############

# Create the dimensions (nCells is the only dimension needed)
nCells = ncfile.createDimension('nCells', CELLCOUNT)     # latitude axis

now = datetime.now()
historyString = now.strftime("%d-%B-%Y %H:%M:%S") + ": File created by " + USER

##############
# ATTRIBUTES #
##############

# Set the attributes
ncfile.title        = "Comparison of icesat freeboard with E3SM"
ncfile.source       = SOURCE
ncfile.history      = historyString
ncfile.institution  = "Los Alamos National Laboratory"

#############
# VARIABLES #
#############

def createVariableForNetCDF(shortName, longName, vmax, vmin = 0.0, fillvalue = None, dtype = np.float64):
    """ Add a variable to the netCDF file. 
    It will appear in the header info. """
    variable = ncfile.createVariable(shortName, dtype, ('nCells',))
    variable.long_name = longName
    variable.valid_range = (vmin, vmax)
    if fillvalue != None:
        variable._fillvalue = fillvalue
    return variable

effmf   = createVariableForNetCDF("effmf", "model freeboard effective sample size", 
                        vmax = 29.88248, fillvalue = -99999.0)
effof   = createVariableForNetCDF("effof", "observed freeboard effective sample size", 
                        vmax = 22321.38, vmin = 0.2787585, fillvalue = -99999.0)
meanmf  = createVariableForNetCDF("meanmf", "model freeboard mean", 
                        vmax = 0.9041953, vmin = 0.01583931, fillvalue = -99999.0)
meanof  = createVariableForNetCDF("meanof", "observed freeboard mean", 
                        vmax = 1.14699, vmin = 0.1046828, fillvalue = -99999.0)
samplemf = createVariableForNetCDF("samplemf", "model freeboard sample count", 
                        vmax = 296)
sampleof = createVariableForNetCDF("sampleof", "observed freeboard sample count", 
                        vmax = 46893)
stdmf   = createVariableForNetCDF("stdmf", "model freeboard standard deviation", 
                        vmax = 0.2506092, vmin = 0.005416268, fillvalue = -99999.0)
stdof   = createVariableForNetCDF("stdof", "observed freeboard standard deviation", 
                        vmax = 0.9629242, vmin = 0.01656876, fillvalue = -99999.0)

########################
# STATISTICAL ANALYSIS #
########################

satelliteFileName = r"\satellite_data_preprocessed\one_day\icesat_E3SM_spring_2008_02_22_16.nc"
satelliteData       = loadData(runDir, satelliteFileName)
freeBoardReadings   = reduceToOneDay(satelliteData, keyVariableToPlot=VARIABLETOPLOT)
cellIndicesForAllSamples      = reduceToOneDay(satelliteData, "modcell")
cellIndicesForAllObservations = returnCellIndices(satelliteData)

############################
# SATELLITE ONLY VARIABLES #
############################
# These variables are easy to pull directly from the satellite data.

# Sample model freeboard is the # of times that cell was passed over 
# (ex. once in a day) in the full time
samplemf[:] = np.bincount(cellIndicesForAllSamples) # Collect one count of the satellite passing overhead.

# Sample observation freeboard is the # of photon reads per cell over full time
sampleof[:] = np.bincount(cellIndicesForAllObservations) # Collect all photon counts into bins using cell indices.

# Observed freeboard mean is the sum of all photon readings 
# in that cell over all time / sampleof
means = []
for cellIndex in range(CELLCOUNT):
    freeBoardIndices = np.where(cellIndicesForAllObservations == cellIndex)[0]
    if freeBoardIndices.size > 0:
        means.append(np.mean(freeBoardIndices))
    else:
        means.append(np.nan)  # Use np.nan for empty cells to indicate missing data
meanof[:] = means

# Model freeboard mean is 
#meanmf = sum of the meanof for that cell over all time / samplemf
#=> hf = hi (ρw-ρi)/ρw + hs (ρw-ρs)/ρw

#######################################
# CALCULATE FREEBOARD FROM MODEL DATA #
#######################################
# TODO: Future work could be to add this variable to E3SM's variables

# E3SM ice volume / E3SM ice area of cell = ice thickness

# height ice + height snow = height water + height of freeboard

# freeboard = ice thickness + snow height - water height (which is 0?)



# Read data back from variable, print min and max
print("-- Min/Max values:", samplemf[:].min(), samplemf[:].max())
print("-- Min/Max values:", sampleof[:].min(), sampleof[:].max())
print("-- Min/Max values:", meanof[:].min(), meanof[:].max())

# close the Dataset
ncfile.close()
print('Dataset is closed!')