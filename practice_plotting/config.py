# Author:   Breanna Powell
# Date:     07/03/2024
# Use this in conjunction with e3sm_data_over_time_visualization.py and e3sm_data_practice_visualization.py
# Make sure to set these variables to the proper file locations.

import os

# Change these for different runs if you want to narrow down your focus
VARIABLETOPLOT  = 'timeDaily_avg_iceAreaCell'   # The variable to plot
LAT_LIMIT       =  50  # Good wide view for the north and south poles; change if you want a wider or narrower view.

# Change these for different runs
runDir         = os.path.dirname(os.path.abspath(__file__))                                  # Get current directory path
meshFileName   = r"\netCDF_files\seaice.EC30to60E2r2.210210.nc"                                       # .nc file for the mesh
outputFileName = r"\netCDF_files\Breanna_D_test_1.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot

# Constants
MAXLONGITUDE    =  180
MINLONGITUDE    = -180
NORTHPOLE       =  90
SOUTHPOLE       = -90

