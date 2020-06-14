#! /usr/bin/env python3

import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
from scipy.fftpack import fft2, ifft2
from mpl_toolkits.mplot3d import Axes3D


# 08-dirtybeam.py takes a dictionary, antArray, of antenna name
# and corresponding (x,y) coordinates, computes the centre of the
# array and determines the uv coverage loci. It is based on
# 07-array2uv-loci.py.
#
# Written by Vasaant S/O Krishnan on Sunday, 14 June 2020





#=====================================================================
#     User variables
#
hourRange = [10, 30]       # Hour angle range of observation (degrees)
srcDec    = 90             # Source declination              (degrees)
steps     = 100            # Resolution for loci
antArray  = {'A' : [ 0.00,  0.10],  # Array coordinates
             'B' : [ 0.00,  0.22],
             'C' : [ 0.00,  0.42],
             'D' : [ 0.00,  0.62],
             'E' : [ 0.00,  0.82],
             'F' : [-0.20, -0.20],
             'G' : [-0.40, -0.40],
             'H' : [-0.60, -0.60],
             'I' : [-0.80, -0.80],
             'J' : [ 0.25, -0.21],
             'K' : [ 0.50, -0.41],
             'L' : [ 0.75, -0.61],
             'M' : [ 1.00, -0.81]}
#=====================================================================





#=====================================================================
#     Functions
def uvDataToTMS(uvdatapoint, hourangle, declinationRadians):
    # Perform the coordinate rotation based on Thompson, Moran &
    # Swenson (2017) equation 4.1:
    us = uvdatapoint[0]*np.sin(hourangle) + uvdatapoint[1]*np.cos(hourangle)
    vs = -uvdatapoint[0]*np.cos(hourangle)*np.sin(declinationRadians) \
         + uvdatapoint[1]*np.sin(hourangle)*np.sin(declinationRadians)
    return [us, vs]
#=====================================================================





#=====================================================================
#     Code begins here
#
maxax = 0     # Axis limits get determined later

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
plt.suptitle('(x, y) to $S(u , v) \\rightarrow B(\\ell , m)$')

# Plot the array configuration
ax1 = fig.add_subplot(221)
for i in antArray:
    ax1.scatter(antArray[i][0], antArray[i][1], c= 'k')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.axis('equal')

hourAngles = np.linspace(np.radians(abs(float(hourRange[0]))), np.radians(abs(float(hourRange[1]))), steps)
srcDecRad  = np.radians(float(srcDec))

# Create arrays to for all baseline & hourAngle permutations
numTerms = len(baseArray)*len(hourAngles)
uvarray = np.ones((numTerms, 2))
vuarray = np.ones((numTerms, 2))

for ind, antPair in enumerate(baseArray):

    # Determine coordinates in uv-plane
    OA = [ a-b for a, b in zip(antArray[antPair[0]], arrayCentre)]    # First  antenna w.r.t centre (e.g. vec{OA})
    OB = [ a-b for a, b in zip(antArray[antPair[1]], arrayCentre)]    # Second antenna w.r.t centre (e.g. vec{OB})
    uv = [-x+y for x, y in zip(OA, OB)]    # vec{AB} = -OA + OB
    vu = [ x-y for x, y in zip(OA, OB)]    # vec{BA} =  OA - OB

    # Set axis limits for plot
    maxuv = max([abs(k) for k in uv])
    if maxuv > maxax:
        maxax = maxuv

    # uv coordinate transformation
    for hangle in np.arange(steps):
        uvarray[hangle*ind] = uvDataToTMS(uv, hourAngles[hangle], srcDecRad)
        vuarray[hangle*ind] = uvDataToTMS(vu, hourAngles[hangle], srcDecRad)

# Plot the sampling pattern
ax2 = fig.add_subplot(222)

ax2.scatter(uvarray[:, 0], uvarray[:, 1], c= 'k', s= 0.3)
ax2.scatter(vuarray[:, 0], vuarray[:, 1], c= 'k', s= 0.3)

ax2.set_xlabel('u')
ax2.set_ylabel('v')
ax2.set_ylim(-maxax, maxax)
ax2.set_xlim(-maxax, maxax)
ax2.axis('equal')
#=====================================================================





#=====================================================================
#     https://stackoverflow.com/questions/50314243/fourier-transform-in-python-2d
#
numCells = steps    # Balance the gridsize by adopting the user's resolution
pltFieldSize = int(2*maxax*numCells)    # Allow plot to range from [-maxax, maxax]
cellSize = 1/float(steps)

Nx, Ny = pltFieldSize, pltFieldSize
range_x, range_y = np.arange(Nx), np.arange(Ny)
dx, dy = cellSize, cellSize
xUV, yUV = dx * (range_x - 0.5*Nx), dy * (range_y - 0.5*Ny)

dBeam_x, dBeam_y = np.pi/np.max(xUV), np.pi/np.max(yUV)
Beam_xUV, Beam_yUV = dBeam_x * np.append(range_x[:Nx//2], -range_x[Nx//2:0:-1]), \
                     dBeam_y * np.append(range_y[:Ny//2], -range_y[Ny//2:0:-1])

x, y = np.meshgrid(xUV, yUV, sparse=False, indexing='ij')
kx, ky = np.meshgrid(Beam_xUV, Beam_yUV, sparse=False, indexing='ij')

# Model the sampling pattern as a surface and toggle each uv point:
f = np.zeros((pltFieldSize, pltFieldSize))
for i, j in zip(uvarray, vuarray):
    xUVal = int((i[0]*numCells)+(numCells*maxax))    # Use y=mx+c to transfrom [-maxax, maxax] --> [0, numCells]
    yUVal = int((i[1]*numCells)+(numCells*maxax))
    if xUVal < pltFieldSize and yUVal < pltFieldSize:
        f[xUVal,yUVal] = 1
    xUVal = int((j[0]*numCells)+(numCells*maxax))
    yUVal = int((j[1]*numCells)+(numCells*maxax))
    if xUVal < pltFieldSize and yUVal < pltFieldSize:
        f[xUVal,yUVal] = 1

F = fft2(f)    # Need to confirm if it is actually fft2 or ifft2
#=====================================================================





#=====================================================================
#     Plotting
#
# The sampling pattern, f
# ax4 = fig.add_subplot(224, projection= '3d')
# surf = ax4.plot_surface(x, y, np.abs(f), cmap= 'binary')
ax4 = fig.add_subplot(224)
ax4.set_title('$S(u , v)$')
ax4.axes.get_xaxis().set_ticks([])
ax4.axes.get_yaxis().set_ticks([])
# ax4.imshow(f, cmap= 'binary')

# The dirty beam, F
ax3 = fig.add_subplot(223, projection= '3d')
# https://stackoverflow.com/questions/11448972/changing-the-background-color-of-the-axes-planes-of-a-matplotlib-3d-plot
ax3.xaxis.pane.fill = False
ax3.yaxis.pane.fill = False
ax3.zaxis.pane.fill = False

# https://stackoverflow.com/questions/59857203/remove-border-from-matplotlib-3d-pane
ax3.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax3.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

ax3.grid(False)
ax3.set_title('$B(\\ell , m)$')
ax3.axes.get_xaxis().set_ticks([])
ax3.axes.get_yaxis().set_ticks([])
ax3.axes.get_zaxis().set_ticks([])

surf = ax3.plot_surface(kx, ky, np.abs(F)*dx*dy, cmap= 'binary')

plt.show()
#=====================================================================
