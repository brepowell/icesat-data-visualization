# Author:   Breanna Powell
# Date:     07/03/2024
# Use this in conjunction with e3sm_data_over_time_visualization.py and e3sm_data_practice_visualization.py
# Make sure to set these variables to the proper file locations.

import os

# Change these for different runs if you want to narrow down your focus
#VARIABLETOPLOT  = 'timeDaily_avg_iceAreaCell'   # The variable to plot from the E3SM data
VARIABLETOPLOT  = 'freeboard'                   # The variable to plot from the satellite data

# Change if you want a wider or narrower view
#LAT_LIMIT       =  50  # Good wide view for the north and south poles for E3SM data
LAT_LIMIT       =  65  # More of a closeup, better for the satellite data

#DOT_SIZE        = 0.4  # Good for the ice area variable
DOT_SIZE        = 7.0  # Good for satellite tracks

# Change these for different runs if you want to grab other .nc files
runDir         = os.path.dirname(os.path.abspath(__file__))       # Get current directory path

meshFileName   = r"\mesh_files\seaice.EC30to60E2r2.210210.nc"    # for 5 day and 10 day simulations
#meshFileName   = r"\mesh_files\mpassi.IcoswISC30E3r5.20231120.nc"     # .nc file for the mesh (doesn't match)

#outputFileName = r"\output_files\Breanna_D_test_1x05_days.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # 5-day Ice Area
#outputFileName = r"\output_files\Breanna_D_test_1x10_days.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc"  # 10-day Ice Area
outputFileName = r"\satellite_data_preprocessed\one_day\icesat_E3SM_spring_2008_02_22_14.nc" # One Satellite Track

# subdirectory = r"/satellite_data_preprocessed/one_month" # Satellite Track folder for one month
#subdirectory = r"/satellite_data_preprocessed/one_week" # Satellite Track folder for one day
subdirectory = r"/satellite_data_preprocessed/one_day" # Satellite Track folder for one day

# Change these to save without overwriting your files
animationFileName   = "satellite_track_2008_02_22_14_animation.gif"   # Should be a .gif extension
mapImageFileName    = "satellite_track_2008_02_22_14.png"             # Should be a .png file extension

# animationFileName   = "satellite_track_2008_02_22_14_animation.gif"   # Should be a .gif extension
# mapImageFileName    = "satellite_track_2008_02_22_14.png"             # Should be a .png file extension

################
# Map settings #
################
boxStyling = dict(boxstyle='round', facecolor='wheat') #other options are alpha (sets transparency)

# These features are on
OCEANFEATURE    = 1   
LANDFEATURE     = 1
COASTLINES      = 1
COLORBARON      = 1
GRIDON          = 1

# These features are off
# N/A

# Constants
MAXLONGITUDE    =  180
MINLONGITUDE    = -180
NORTHPOLE       =  90
SOUTHPOLE       = -90

