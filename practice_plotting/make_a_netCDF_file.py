# Breanna Powell
# Created: 07/17/2024

# This is a great tutorial about writing netCDF files:
# https://unidata.github.io/python-training/workshop/Bonus/netcdf-writing/

import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import os

USER    = os. getlogin()                        #TODO: check if this is ok
SOURCE  = "SOME PATH NAME TO FILL IN LATER"     #TODO: make this dynamic

#TODO: Make sure the data types are correct; there should be an "f" after many of them.

try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset('new.nc',mode='w',format='NETCDF4_CLASSIC') 

# Create the dimensions (nCells is the only dimension needed)
nCells = ncfile.createDimension('nCells', 235160)     # latitude axis

def createVariableForNetCDF(shortName, longName, vmax, vmin = 0.0, fillvalue = None, dtype = np.float64):
    variable = ncfile.createVariable(shortName, dtype, ('nCells',))
    variable.long_name = longName
    variable.valid_range = (vmin, vmax)
    if fillvalue != None:
        variable._fillvalue = fillvalue
    return variable

createVariableForNetCDF("effmf", "model freeboard effective sample size", 
                        vmax = 29.88248, fillvalue = -99999.0)
createVariableForNetCDF("effof", "observed freeboard effective sample size", 
                        vmax = 22321.38, vmin = 0.2787585, fillvalue = -99999.0)
createVariableForNetCDF("meanmf", "model freeboard mean", 
                        vmax = 0.9041953, vmin = 0.01583931, fillvalue = -99999.0)
createVariableForNetCDF("meanof", "observed freeboard mean", 
                        vmax = 1.14699, vmin = 0.1046828, fillvalue = -99999.0)
createVariableForNetCDF("samplemf", "model freeboard sample count", 
                        vmax = 296)
createVariableForNetCDF("sampleof", "observed freeboard sample count", 
                        vmax = 46893)
createVariableForNetCDF("stdmf", "model freeboard standard deviation", 
                        vmax = 0.2506092, vmin = 0.005416268, fillvalue = -99999.0)
createVariableForNetCDF("stdof", "observed freeboard standard deviation", 
                        vmax = 0.9629242, vmin = 0.01656876, fillvalue = -99999.0)

now = datetime.now()
historyString = now.strftime("%d-%B-%Y %H:%M:%S") + ": File created by " + USER

# Set the attributes
ncfile.title        = "Comparison of icesat freeboard with E3SM"
ncfile.source       = SOURCE
ncfile.history      = historyString
ncfile.institution  = "Los Alamos National Laboratory"

# close the Dataset
ncfile.close()
print('Dataset is closed!')