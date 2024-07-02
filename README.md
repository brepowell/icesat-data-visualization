﻿# icesat2-data-visualization
The purpose of this repository is to store visualization tools for me to use when looking at data from icesat-2 and E3SM. There is another repository where I cloned E3SM. I will be creating a new analysis member for E3SM this summer.

## plotting_library_practice
This folder contains some generic matplotlib and cartopy examples that I used to give me a better feel for how those libraries work and what they are capable of doing.

## practice_plotting
This folder has my initial mapping of some netCDF files. 

e3sm_data_practice_visualization.py is where I put several utility functions to use to create simple maps of the north and south pole and overlay them with scatterplots of e3sm data. 

e3sm_data_over_time_visualization.py is where I made a function to create an animation for however many days exist in the netCDF file.

icesat2_data_practice_visualization.py is where I first queried the NASA satellite, icesat-2. That part of the project is on hiatus as other parts of the project have taken priority.
