#! /usr/bin/env python

import matplotlib.pyplot as plt
from itertools import combinations

# 06-array2uv.py takes a dictionary, antArray, of antenna name and
# corresponding (x,y) coordinates, computes the centre of the array
# and determines the instantaneous uv coverage.
#
# Written by Vasaant S/O Krishnan on Saturday, 25 May 2019





#=====================================================================
#     User variables
#
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

plt.show()
#=====================================================================
