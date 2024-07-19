from utility import *

runDir         = os.path.dirname(os.path.abspath(__file__))       # Get current directory path

outputFileName   = r"\mesh_files\mpassi.IcoswISC30E3r5.20231120.nc"

# Checking the sizes for the number of grid cells per .nc file
# outputFileName = r"\mesh_files\DECK_Coast.nc"                     # Size in grid cells: 18157
# outputFileName = r"\mesh_files\E3SM_DECK_Emulator_File.nc"        # Size in grid cells: 235160
# outputFileName = r"\mesh_files\E3SM_V1_C_grid_Coast.nc"           # Size in grid cells: 74686
# outputFileName = r"\mesh_files\ICESat_Masked_E3SM.nc"             # Size in grid cells: 6220

# FILES FOR 5 OR 10 DAY SIMULATION:
# outputFileName = r"\mesh_files\seaice.EC30to60E2r2.210210.nc"     # Size in grid cells: 236853
#outputFileName = r"\output_files\Breanna_D_test_1x05_days.mpassi.hist.am.timeSeriesStatsDaily.0001-01-01.nc" # 236853

# FILES FOR 1 YEAR SIMULATION:
# outputFileName = r"\mesh_files\mpassi.IcoswISC30E3r5.20231120.nc" # Size in grid cells:     465044

# FILES FOR SATELLITE TRACK ANIMATION:
#outputFileName = r"\satellite_data_preprocessed\one_day\icesat_E3SM_spring_2008_02_22_16.nc"  # 6533

output = loadData(runDir, outputFileName)
printAllAvailableVariables(output)