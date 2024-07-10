# Author:   Breanna Powell
# Date:     07/03/2024
# Use this in conjunction with e3sm_data_over_time_visualization.py and e3sm_data_practice_visualization.py
# Make sure to set these variables to the proper file locations.

import os

# Change these for different runs if you want to narrow down your focus
# VARIABLETOPLOT  = 'timeDaily_avg_iceAreaCell'   # The variable to plot
VARIABLETOPLOT  = 'freeboard'

#'cell' # Gets the index that corresponds to the mesh file

LAT_LIMIT       =  50  # Good wide view for the north and south poles; change if you want a wider or narrower view.

# Change these for different runs if you want to grab other .nc files
runDir         = os.path.dirname(os.path.abspath(__file__))       # Get current directory path

meshFileName   = r"\mesh_files\seaice.EC30to60E2r2.210210.nc"    # for 5 day and 10 day simulations
#meshFileName   = r"\mesh_files\mpassi.IcoswISC30E3r5.20231120.nc"     # .nc file for the mesh

#outputFileName = r"\output_files\Breanna_D_test_1x10_days.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # .nc file for the data to plot
outputFileName = r"\satellite_data_preprocessed\icesat_E3SM_spring_2008_02_22_16.nc" # Satellite Track

# Change these to save without overwriting your files
animationFileName   = "satellite_track_2008_02_22_16_animation.gif"             # Should be a .gif extension
mapImageFileName    = "satellite_track_2008_02_22_16.png"             # Should be a .png file extension

# Constants
MAXLONGITUDE    =  180
MINLONGITUDE    = -180
NORTHPOLE       =  90
SOUTHPOLE       = -90

