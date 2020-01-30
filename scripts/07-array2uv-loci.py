#! /usr/bin/env python

import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np

# 07-array2uv-loci.py takes a dictionary, antArray, of antenna name
# and corresponding (x,y) coordinates, computes the centre of the
# array and determines the uv coverage loci. It is based on
# 06-array2uv.py.
#
# Written by Vasaant S/O Krishnan on Tuesday, 25 June 2019.





#=====================================================================
#     User variables
#

hourRange = [10, 35]       # Hour angle range of observation (degrees)
srcDec    = 10             # Source declination              (degrees)
steps     = 300            # Resolution for loci
antArray  = {'A' : [ 0.5, -0.5],  # Array coordinates
             'B' : [   0,  0.5],
             'C' : [-2.5, -0.7]}

#=====================================================================





#=====================================================================
#     Code begins here
#

# Determine all unique baselines
baseArray = [','.join(map(str, comb)).split(',') for comb in combinations(antArray.keys(), 2)]

# Determine centre of array from all antennas
numAnts = float(len(antArray))
xAntCoords = 0
yAntCoords = 0
for i in antArray:
    xAntCoords += antArray[i][0]
    yAntCoords += antArray[i][1]
arrayCentre = [xAntCoords/numAnts, yAntCoords/numAnts]
#=====================================================================





#=====================================================================
#     Compute verctors and plot
#
fig = plt.figure()
plt.suptitle('(x, y) to (u, v)')

# Plot the array configuration
ax1 = fig.add_subplot(121)
for i in antArray:
    ax1.scatter(antArray[i][0], antArray[i][1], c= 'k')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

hourAngles = np.linspace(np.radians(abs(float(hourRange[0]))), np.radians(abs(float(hourRange[1]))), steps)
srcDecRad  = np.radians(float(srcDec))

# Plot the sampling pattern
ax2 = fig.add_subplot(122)
for i in baseArray:

    # Determine coordinates in uv-plane
    OA = [ a-b for a, b in zip(antArray[i[0]], arrayCentre)]   # First  antenna w.r.t centre (e.g. vec{OA})
    OB = [ a-b for a, b in zip(antArray[i[1]], arrayCentre)]   # Second antenna w.r.t centre (e.g. vec{OB})
    uv = [-x+y for x, y in zip(OA, OB)]                        # vec{AB} = -OA + OB
    vu = [ x-y for x, y in zip(OA, OB)]                        # vec{BA} =  OA - OB

    ax2.scatter(uv[0], uv[1], c= 'k')
    ax2.scatter(vu[0], vu[1], c= 'k')
    ax2.set_xlabel('u')
    ax2.set_ylabel('v')

    # Perform the coordinate rotation based on Thompson, Moran & Swenson (2017) equation 4.1:
    for hangle in hourAngles:
        us = [ uv[0]*np.sin(hangle) + uv[1]*np.cos(hangle)]
        vs = [-uv[0]*np.cos(hangle)*np.sin(srcDecRad) + uv[1]*np.sin(hangle)*np.sin(srcDecRad)]
        ax2.scatter(us, vs, c= 'b')

        us = [ vu[0]*np.sin(hangle) + vu[1]*np.cos(hangle)]
        vs = [-vu[0]*np.cos(hangle)*np.sin(srcDecRad) + vu[1]*np.sin(hangle)*np.sin(srcDecRad)]
        ax2.scatter(us, vs, c= 'b')

plt.show()
# #=====================================================================
