from config import *
from utility import *
from e3sm_data_visualization import *
from make_a_netCDF_file import *

def generateNorthPoleStaticPlotOfTrackLatLong(fig, northMap, mapImageFileName, grid=GRIDON,
                         oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, 
                         coastlines=COASTLINES):
    """ Just plot the lat and long of the satellite tracks from multiple satellite files."""

    fileList = returnListOfSatFileNamesBySeasonAndYear("fall", 2008)
    print("Number of files read: ", len(fileList))

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

    for file in fileList:
        print("Satellite file: ", file)
        satelliteData       = loadData("", file) #PM
        latCell, lonCell    = getLatLon(satelliteData)
        scatter = mapNorthernHemisphere(latCell, lonCell, "Arctic_lat_long", northMap, 0.05)     # Map northern hemisphere

    plt.suptitle("lat and long", size="x-large", fontweight="bold")

    # Save the maps as an image.
    plt.savefig(mapImageFileName)
    print("Saved .png")

    return scatter

def main ():

    fig, northMap = generateNorthPoleAxes()
    generateNorthPoleStaticPlotOfTrackLatLong(fig, northMap, mapImageFileName, grid=GRIDON,
                         oceanFeature=OCEANFEATURE, landFeature=LANDFEATURE, 
                         coastlines=COASTLINES)
