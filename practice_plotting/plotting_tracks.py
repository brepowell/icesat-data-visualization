from config import *
from utility import *
from e3sm_data_visualization import *
from make_a_netCDF_file import *


def generateNorthPoleStaticPlotOfTrackLatLong(fig, northMap, mapImageFileName, grid=GRIDON,
                         oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, 
                         coastlines=COASTLINES):
    """ Just plot the lat and long of the satellite tracks from multiple satellite files."""

    # SPRING 2003 ONLY - make sure to set stoppingPoint = 409
    filenamePattern = f"icesat_E3SM_spring_2003_{str(month).zfill(2)}_{str(day).zfill(2)}_{str(hour).zfill(2)}.nc"   

    searchPattern = os.path.join(perlmutterpathSatellites, filenamePattern)
    matchingFiles = glob.glob(searchPattern)
    satelliteFileName = matchingFiles[0] if matchingFiles else None
    print("Matching files: ", matchingFiles)

    print("Satellite file name: ", satelliteFileName)

    #satelliteData       = loadData(runDir, satelliteFileName)
    satelliteData       = loadData("", satelliteFileName) #PM

    freeBoardReadings               = reduceToOneDay(satelliteData, "freeboard")
    cellIndicesForAllSamples        = returnCellIndices(satelliteData, "modcell")
    cellIndicesForAllObservations   = returnCellIndices(satelliteData, "cell")

    output = loadData(runDir, outputFileName)
    latCell, lonCell = getLatLon(output)

    # Adjust the margins around the plots (as a fraction of the width or height).
    fig.subplots_adjust(bottom=0.05, top=0.85, left=0.04, right=0.95, wspace=0.02)

    # Set your viewpoint (the bounding box for what you will see).
    # You want to see the full range of longitude values, since this is a polar plot.
    # The range for the latitudes should be from your latitude limit (i.e. 50 degrees or -50 to the pole at 90 or -90).
    northMap.set_extent([MINLONGITUDE, MAXLONGITUDE, LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())

    # Add map features, like landFeature and oceanFeature.
    addMapFeatures(northMap, oceanFeature, landFeature, grid, coastlines)

    # Crop the map to be round instead of rectangular.
    northMap.set_boundary(makeCircle(), transform=northMap.transAxes)

    # Map the hemisphere
    scatter = mapNorthernHemisphere(latCell, lonCell, "Arctic_lat_long", northMap, 0.05)     # Map northern hemisphere

    plt.suptitle("lat and long", size="x-large", fontweight="bold")

    # Save the maps as an image.
    plt.savefig(mapImageFileName)

    return scatter


def main ():

    fileCount, timeStrings, timeCluster, timeYear, timeMonth, timeDay, timeHour, timeGregorian = loadSynchronizer()
