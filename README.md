# icesat-data-visualization
The purpose of this repository is to store visualization tools for me to use when looking at data from the DOE's Energy Exascale System Model (E3SM) and NASA's IceSat or IceSat-2. There is another repository on my github where I forked E3SM. I will be creating a new analysis member for E3SM this summer within that forked repo.

## plotting_library_practice
This folder contains some generic matplotlib and cartopy examples that I used to give me a better feel for how those libraries work and what they are capable of doing.

## practice_plotting
This folder has my initial mapping of some netCDF files. 

e3sm_data_visualization.py is where I put several utility functions to use to create simple maps of the north and south pole and overlay them with scatterplots of e3sm data. 

<img src="\practice_plotting\images_and_animations\seaice_both_poles.png" width = "400">

<img src="\practice_plotting\images_and_animations\seaice_north_pole.png" width = "400">

e3sm_data_over_time_visualization.py is where I made a function to create an animation for however many days exist in the netCDF file.

> Here's a 5-day simulation, where blue is water and red is sea ice; white is a border between the two

<img src="\practice_plotting\images_and_animations\5_day_simulation.gif" width = "400">

> Here's a 10-day simulation; both of these start from initial conditions, which are perfect. That is why there is a very nice edge at first.

<img src="\practice_plotting\images_and_animations\10_day_simulation.gif" width = "400">

plotting_track_animation.py is where I plot the path of one satellite track as it travels over the Arctic.

> Here's an animated version of the satellite path:

<img src="\practice_plotting\images_and_animations\satellite_track_2008_02_22_14_animation.gif" width = "400">

> Here's a static version of the satellite path:

<img src="\practice_plotting\images_and_animations\satellite_track_2008_02_22_14.png" width = "400">

plotting_track_animation_over_time.py is where I plot the path of one satellite track as it travels over the Arctic for a day or month. Note that a month takes a while to run.

> Here's an animated version of the satellite paths for one day:

<img src="\practice_plotting\images_and_animations\satellite_track_2008_02_22_day_animation.gif" width = "400">

> Here's a static version of the satellite paths for one day:

<img src="\practice_plotting\images_and_animations\satellite_track_2008_02_22_day.png" width = "400">

Here is the same program running for one week.

<img src="\practice_plotting\images_and_animations\satellite_track_2005_03_01_week_animation.gif" width = "400">

icesat2_data_practice_visualization.py is where I first queried NASA satellite ICESat-2. That part of the project is on hiatus as other parts of the project have taken priority.
