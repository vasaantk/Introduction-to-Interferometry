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

antArray = {'M000' :[21.44380306, -30.71292524],
            'M001' :[21.44390085, -30.71260539],
            'M002' :[21.44355442, -30.71307843],
            'M003' :[21.44319474, -30.71288049],
            'M004' :[21.44259918, -30.71333651000001],
            'M005' :[21.44282392, -30.71360891],
            'M006' :[21.44369852, -30.71372031],
            'M007' :[21.4429543, -30.71468778],
            'M008' :[21.44291274, -30.71588095],
            'M009' :[21.44422681, -30.71440232],
            'M010' :[21.444809, -30.71567238],
            'M011' :[21.44476593, -30.7142314],
            'M012' :[21.44535056, -30.71437675],
            'M013' :[21.44636072, -30.71460427],
            'M014' :[21.44681895, -30.71363265999999],
            'M015' :[21.44608845, -30.71303153],
            'M016' :[21.44689743, -30.71273217],
            'M017' :[21.44597304, -30.71206826],
            'M018' :[21.44499267, -30.71327305000001],
            'M019' :[21.44567218, -30.71362797000001],
            'M020' :[21.44490234, -30.71375803000001],
            'M021' :[21.44079994, -30.71400721],
            'M022' :[21.44052529, -30.71233809],
            'M023' :[21.43999592, -30.71105094],
            'M024' :[21.44022471, -30.70970248],
            'M025' :[21.44198987, -30.70902091],
            'M026' :[21.44285617, -30.71090172],
            'M027' :[21.44431225, -30.71126445],
            'M028' :[21.44335543, -30.71184184],
            'M029' :[21.44296272, -30.71217469],
            'M030' :[21.44567669, -30.7100276],
            'M031' :[21.44646253, -30.71021016],
            'M032' :[21.44870382, -30.7094729],
            'M033' :[21.44995027, -30.70326373],
            'M034' :[21.44762369, -30.71131072],
            'M035' :[21.44792048, -30.71268726],
            'M036' :[21.44794236, -30.71367768],
            'M037' :[21.447859, -30.71519796000001],
            'M038' :[21.44611607, -30.71618829],
            'M039' :[21.44653843, -30.71639649],
            'M040' :[21.44360936, -30.71747896],
            'M041' :[21.440888, -30.71702307],
            'M042' :[21.44011369, -30.71520674],
            'M043' :[21.43731453, -30.71221265],
            'M044' :[21.43453602, -30.70564016],
            'M045' :[21.42475874, -30.70864938],
            'M046' :[21.42857562, -30.69525542],
            'M047' :[21.43785295, -30.71572093],
            'M048' :[21.4146123, -30.68682094],
            'M049' :[21.40625266, -30.70711438],
            'M050' :[21.42246555, -30.71866252],
            'M051' :[21.43501372, -30.7179944],
            'M052' :[21.43769653, -30.72141485],
            'M053' :[21.44398726, -30.72281975],
            'M054' :[21.45299144, -30.71556328],
            'M055' :[21.45643282, -30.7101845],
            'M056' :[21.46057174, -30.70684555],
            'M057' :[21.44696358, -30.68165598],
            'M058' :[21.4731677, -30.68682094],
            'M059' :[21.48236368, -30.7042055],
            'M060' :[21.47958867, -30.72764899],
            'M061' :[21.44371766, -30.73201279],
            'M062' :[21.42884892, -30.73363457],
            'M063' :[21.40819133, -30.72764899]}
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

numTerms = len(baseArray)
uvarray = np.zeros((numTerms, 2))
#=====================================================================





#=====================================================================
#     Plotting
#
fig = plt.figure(figsize=(15, 7.5))
plt.suptitle('(x, y) to (u, v)', fontsize= textsize)

ax1 = fig.add_subplot(121)
for i in antArray:
    ax1.scatter(antArray[i][0], antArray[i][1], s= 20, c= 'k')
ax1.set_xlabel('x', fontsize= textsize)
ax1.set_ylabel('y', fontsize= textsize)
ax1.tick_params(axis='both', which='both', labelsize= textsize)
ax1.axis('equal')

ax2 = fig.add_subplot(122)
for index, antPair in enumerate(baseArray):
    # Determine coordinates in uv-plane
    OA = [ a-b for a, b in zip(antArray[antPair[0]], arrayCentre)]    # First  antenna w.r.t centre (e.g. vec{OA})
    OB = [ a-b for a, b in zip(antArray[antPair[1]], arrayCentre)]    # Second antenna w.r.t centre (e.g. vec{OB})
    uv = [-x+y for x, y in zip(OA, OB)]    # vec{AB} = -OA + OB

    # uv coordinate transformation
    uvarray[index] = uv

# Get axis limits for plot
maxax = np.ceil(np.amax(np.abs(uvarray)))

# Plot the sampling pattern, S(u, v)
ax2.scatter(uvarray[:, 0], uvarray[:, 1], c= 'k', s= 3)
ax2.scatter(-uvarray[:, 0], -uvarray[:, 1], c= 'k', s= 3)
ax2.set_xlabel('u', fontsize= textsize)
ax2.set_ylabel('v', fontsize= textsize)
ax2.tick_params(axis='both', which='both', labelsize= textsize)
ax2.axis('equal')

# plt.savefig('06-array2uv-meerkat.eps', transparent=True, format='eps')
plt.show()
#=====================================================================
