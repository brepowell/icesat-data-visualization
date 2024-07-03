# Work in progress

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
from e3sm_data_practice_visualization import *


def mapTrack(latCell, lonCell, variableToPlot1Day, title, hemisphereMap):

    indices = np.where(latCell > LAT_LIMIT)

    sc = hemisphereMap.scatter(lonCell[indices], latCell[indices], c=variableToPlot1Day[indices], cmap='bwr', s=0.4, transform=ccrs.PlateCarree())
    hemisphereMap.set_title(title)
    hemisphereMap.axis('off')

    return sc

def generatePoleMaps(fig, northMap, latCell, lonCell, variableToPlot1Day, mapImageFileName, colorBarOn=1, oceanFeature=1, landFeature=1, grid=1, coastlines=1):
    """ Generate 2 maps; one of the north pole and one of the south pole. """

    # Adjust the margins around the plots (as a fraction of the width or height).
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

    # Set your viewpoint (the bounding box for what you will see).
    # You want to see the full range of longitude values, since this is a polar plot.
    # The range for the latitudes should be from your latitude limit (i.e. 50 degrees or -50 to the pole at 90 or -90).
    northMap.set_extent([MINLONGITUDE, MAXLONGITUDE,  LAT_LIMIT, NORTHPOLE], ccrs.PlateCarree())

    # Add map features, like landFeature and oceanFeature.
    addMapFeatures(northMap, oceanFeature, landFeature, grid, coastlines)

    # Crop the map to be round instead of rectangular.
    northMap.set_boundary(makeCircle(), transform=northMap.transAxes)

    # Map the 2 hemispheres.
    northPoleScatter = mapTrack(latCell, lonCell, variableToPlot1Day, "n", "Arctic Sea Ice", northMap)     # Map northern hemisphere

    # Set Color Bar
    if colorBarOn:
        plt.colorbar(northPoleScatter, ax=northMap)

    # Save the maps as an image.
    plt.savefig(mapImageFileName)

    return northPoleScatter

# def update(frame):
#     # for each frame, update the data stored on each artist.
#     x = t[:frame]
#     y = z[:frame]
    
#     # update the scatter plot:
#     data = np.stack([x, y]).T
#     scat.set_offsets(data)
#     return (scat)

# ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
# plt.show()

# ani.save(filename="example.gif", writer="pillow")