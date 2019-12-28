#! /usr/bin/env python

import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np

# 06-array2uv.py takes a dictionary, antArray, of antenna name and
# corresponding (x,y) coordinates, computes the centre of the array
# and determines the instantaneous uv coverage.
#
# Written by Vasaant S/O Krishnan on Saturday, 25 May 2019





#=====================================================================
#     User variables
#
textsize = 13
annotateSize = 10
hourRange = [10, 20]       # Hour angle range of observation (degrees)
srcDec    = 90             # Source declination              (degrees)
steps     = 300
antArray = {'A' : [ 0.5, -0.5],
            'B' : [   0,  0.5],
            'C' : [-0.5, -0.5]}
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
#     Plotting
#
fig = plt.figure(figsize=(15, 7.5))
plt.suptitle('(x, y) to (u, v)', fontsize= textsize)

# Plot the array configuration
ax1 = fig.add_subplot(121)
for i in antArray:
    ax1.scatter(antArray[i][0], antArray[i][1], s= 20, c= 'k')
    ax1.set_xlabel('x', fontsize= textsize)
    ax1.set_ylabel('y', fontsize= textsize)
    ax1.tick_params(axis='both', which='both', labelsize= textsize)
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)

    # Labels for individual points
    pointLabel = i + ' (' + str(antArray[i][0]) + ', ' + str(antArray[i][1]) + ')'
    ax1.annotate(pointLabel , xy= (antArray[i][0] + 0.1, antArray[i][1]), size= annotateSize)
    ax1.scatter(0, 0, s= 20, c= 'k', marker= 'x', alpha= 0.3)
    ax1.annotate('O (0, 0)' , xy= (0 + 0.1, 0), size= annotateSize)

hourAngles = np.linspace(np.radians(float(hourRange[0])), np.radians(float(hourRange[1])), steps)
srcDecRad  = np.radians(float(srcDec))

# Plot the sampling pattern
ax2 = fig.add_subplot(122)
for i in baseArray:
    # Determine coordinates in uv-plane
    OA = [ a-b for a, b in zip(antArray[i[0]], arrayCentre)]    # First  antenna w.r.t centre (e.g. vec{OA})
    OB = [ a-b for a, b in zip(antArray[i[1]], arrayCentre)]    # Second antenna w.r.t centre (e.g. vec{OB})
    uv = [-x+y for x, y in zip(OA, OB)]                         # vec{AB} = -OA + OB
    vu = [ x-y for x, y in zip(OA, OB)]                         # vec{BA} =  OA - OB

    ax2.scatter(uv[0], uv[1], s= 20, c= 'k')
    ax2.scatter(vu[0], vu[1], s= 20, c= 'k')
    ax2.set_xlabel('u', fontsize= textsize)
    ax2.set_ylabel('v', fontsize= textsize)
    ax2.tick_params(axis='both', which='both', labelsize= textsize)
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)

    # Perform the coordinate rotation based on Thompson, Moran & Swenson (2017) equation 4.1:
    for hangle in hourAngles:
        us = [ uv[0]*np.sin(hangle) + uv[1]*np.cos(hangle)]
        vs = [-uv[0]*np.cos(hangle)*np.sin(srcDecRad) + uv[1]*np.sin(hangle)*np.sin(srcDecRad)]
        ax2.scatter(us, vs, c= 'b')

        us = [ vu[0]*np.sin(hangle) + vu[1]*np.cos(hangle)]
        vs = [-vu[0]*np.cos(hangle)*np.sin(srcDecRad) + vu[1]*np.sin(hangle)*np.sin(srcDecRad)]
        ax2.scatter(us, vs, c= 'b')

    # Labels for individual points
    pointLabel = '$\\overrightarrow{%s%s}$'%(i[0], i[1]) # + ' (' + str(uv[0]) + ', ' + str(uv[1]) + ')'
    ax2.annotate(pointLabel , xy= (uv[0] + 0.1, uv[1]), size= annotateSize)
    pointLabel = '$\\overrightarrow{%s%s}$'%(i[1], i[0]) # + ' (' + str(vu[0]) + ', ' + str(vu[1]) + ')'
    ax2.annotate(pointLabel , xy= (vu[0] + 0.1, vu[1]), size= annotateSize)

# plt.savefig('06-array2uv-triangle.eps', transparent=True, format='eps')
plt.show()
#=====================================================================
