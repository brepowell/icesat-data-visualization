# icesat-data-visualization
The purpose of this repository is to store visualization tools for me to use when looking at data from the DOE's Energy Exascale System Model (E3SM) and NASA's IceSat or IceSat-2. There is another repository on my github where I forked E3SM. I will be creating a new analysis member for E3SM this summer within that forked repo.

## plotting_library_practice
This folder contains some generic matplotlib and cartopy examples that I used to give me a better feel for how those libraries work and what they are capable of doing.

## practice_plotting
This folder has my initial mapping of some netCDF files. 

e3sm_data_practice_visualization.py is where I put several utility functions to use to create simple maps of the north and south pole and overlay them with scatterplots of e3sm data. 

<img src="\practice_plotting\seaice_both_poles.png" width = "400">

<img src="\practice_plotting\seaice_north_pole.png" width = "400">

e3sm_data_over_time_visualization.py is where I made a function to create an animation for however many days exist in the netCDF file.

icesat2_data_practice_visualization.py is where I first queried the NASA satellite, icesat-2. That part of the project is on hiatus as other parts of the project have taken priority.
