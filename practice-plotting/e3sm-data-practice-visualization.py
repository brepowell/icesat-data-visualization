# Breanna Powell
# Modified code from Mark Petersen and Savannah Byron

##########
# TO RUN #
##########

# Make sure that you navigate to the directory that contains e3sm-data-practice-visualization.py
# Have a folder labeled "data" in that directory
# The data folder must contain the mesh file and the output file
# Ensure that you are looking for a variable that exists in the output file
# $ python e3sm-data-practice-visualization.py

import os
import math
import numpy as np
import xarray
import matplotlib as mpl
import matplotlib.pyplot as plt

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.mpl.ticker as cticker
import cartopy.feature as cfeature

# Change these for different runs
runDir = os.path.dirname(os.path.abspath(__file__))     # Gets the current directory path
meshFileName = "\data\seaice.EC30to60E2r2.210210.nc"                                         # .nc file for the mesh
outputFileName = "\data\Breanna_D_test_1.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot
varToPlot = 'timeDaily_avg_iceAreaCell' # The variable that you want to plot

# Create a figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(20, 8))
leftMap = axs[0]
rightMap = axs[1]

print('read: ', runDir, meshFileName)
mesh = xarray.open_dataset(runDir + meshFileName)
nCells = mesh.sizes['nCells']
latCell = mesh.variables['latCell'] # in radians
lonCell = mesh.variables['lonCell']
xCell = mesh.variables['xCell'] # in meters
yCell = mesh.variables['yCell']

print('read: ', runDir, outputFileName)
output = xarray.open_dataset(runDir + outputFileName)

var = output.variables[varToPlot]

# reduce the variable to 1D so we can use these indices
var1D = var[0,:]

#######################
# Northern Hemisphere #
#######################

NorthernHemisphereIndices = np.where(latCell > math.radians(60))

# Plot Arctic data in the first subplot
sc = leftMap.scatter(xCell[NorthernHemisphereIndices], yCell[NorthernHemisphereIndices], c=var1D[NorthernHemisphereIndices], cmap='bwr', s=0.4)
leftMap.set_title('Arctic Sea Ice')
leftMap.axis('off')
plt.colorbar(sc, ax=leftMap)

#######################
# Southern Hemisphere #
#######################

SouthernHemisphereIndices = np.where(latCell < math.radians(-60))

# Plot Antarctic data in the second subplot
sc = rightMap.scatter(yCell[SouthernHemisphereIndices], xCell[SouthernHemisphereIndices], c=var1D[SouthernHemisphereIndices], cmap='bwr', s=0.4)
rightMap.set_title('Antarctic Sea Ice')
plt.colorbar(sc, ax=rightMap)

plt.axis('off')

###############
# Save figure #
###############

plt.savefig('seaice_Output.png')
