#! /usr/bin/env python3

import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift
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
hourRange = [10, 30]        # Hour angle range of observation (degrees)
srcDec    = 85              # Source declination              (degrees)
steps     = 500             # Resolution for loci
antArray  = {'A' : [ 0.05,  0.10],  # Array coordinates
             'B' : [-0.07,  0.22],
             'C' : [ 0.00,  0.42],
             'D' : [ 0.02,  0.62],
             'E' : [-0.10,  0.82],
             'F' : [-0.20, -0.20],
             'G' : [-0.40, -0.25],
             'H' : [-0.60, -0.66],
             'I' : [-0.80, -0.80],
             'J' : [ 0.25, -0.21],
             'K' : [ 0.50, -0.05],
             'L' : [ 0.50, -0.41],
             'M' : [ 0.75, -0.75],
             'O' : [ 2.75, -1.75],
             'N' : [ 1.00, -0.81]}
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
# Determine all unique baselines
baseArray = [','.join(map(str, comb)).split(',') for comb in
             combinations(antArray.keys(), 2)]

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
plt.suptitle(
    'Array Layout to Sampling Pattern and Dirty Beam\n $S(u , v) \\rightarrow B(\\ell , m)$')

# Plot the array configuration
ax1 = fig.add_subplot(221)
for i in antArray:
    ax1.scatter(antArray[i][0], antArray[i][1], c= 'k')
ax1.set_title('Array layout')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.axis('equal')

hourAngles = np.linspace(np.radians(abs(float(hourRange[0]))),
                         np.radians(abs(float(hourRange[1]))), steps)
srcDecRad  = np.radians(float(srcDec))

# Create arrays for all baseline & hourAngle permutations
numTerms = len(baseArray)*len(hourAngles)
uvarray = np.zeros((numTerms, 2))

for index, antPair in enumerate(baseArray):

    # Determine coordinates in uv-plane
    OA = [ a-b for a, b in zip(antArray[antPair[0]], arrayCentre)]    # First  antenna w.r.t centre (e.g. vec{OA})
    OB = [ a-b for a, b in zip(antArray[antPair[1]], arrayCentre)]    # Second antenna w.r.t centre (e.g. vec{OB})
    uv = [-x+y for x, y in zip(OA, OB)]    # vec{AB} = -OA + OB

    # uv coordinate transformation
    for hangle in np.arange(steps):
        uvarray[hangle*index] = uvDataToTMS(uv, hourAngles[hangle], srcDecRad)

# Get axis limits for plot
maxax = np.ceil(np.amax(np.abs(uvarray)))

# Plot the sampling pattern, S(u, v)
ax2 = fig.add_subplot(222)
ax2.scatter(uvarray[:, 0], uvarray[:, 1], c= 'k', s= 0.3)
ax2.scatter(-uvarray[:, 0], -uvarray[:, 1], c= 'k', s= 0.3)

ax2.set_title('$S(u, v)$')
ax2.set_xlabel('u')
ax2.set_ylabel('v')
ax2.set_ylim(-maxax, maxax)
ax2.set_xlim(-maxax, maxax)
ax2.axis('equal')
#=====================================================================





#=====================================================================
#     Grid the uv and vu sampling points
#
numCells = np.sqrt(steps)    # Balance the gridsize by adopting the user's resolution
pltFieldSize = int(2*maxax*numCells)    # Allow plot to range from [-maxax, maxax]

# Model the sampling pattern as a surface...
sky = np.zeros((pltFieldSize, pltFieldSize))
# sky[ 0,  0] = TLC
# sky[ 0, -1] = TRC
# sky[-1,  0] = BLC
# sky[-1, -1] = BRC

# Use y=mx+c to transfrom [-maxax, maxax] --> [0, numCells]
uvToGrid = lambda x: int((x*numCells)+(numCells*maxax))

#... and toggle each uv point
vuarray = -uvarray
for i, j in zip(uvarray, vuarray):
    xUVpt = uvToGrid(i[0])
    yUVpt = uvToGrid(i[1])
    sky[yUVpt, xUVpt] = 1

    xVUpt = uvToGrid(j[0])
    yVUpt = uvToGrid(j[1])
    sky[yVUpt, xVUpt] = 1

f = np.flip(sky, 0)    # uvToGrid does not totally work, so I must flip the axis, f = S(u, v)
F = ifft2(f)    # Take the Inverse Fourier Transform to get B(l, m)
#=====================================================================





#=====================================================================
#     Plotting in 2D
#
# The sampling pattern, f = S(u, v)
ax4 = fig.add_subplot(224)
ax4.set_title('$S(u, v)$ gridded')
ax4.imshow(f, cmap= 'binary')

# The dirty beam, F = B(l, m)
ax3 = fig.add_subplot(223)
ax3.set_title('$B(\\ell , m)$')
ax3.imshow(np.abs(fftshift(F)), cmap= 'binary')    # Note the fftshift

plt.show()
#=====================================================================





# #=====================================================================
# #     Plotting in 3D
# #     Based on "fourier-transform-in-python-2d"
# #     https://stackoverflow.com/questions/50314243/
# #
# cellSize = 1/float(steps)

# Nx, Ny = pltFieldSize, pltFieldSize
# range_x, range_y = np.arange(Nx), np.arange(Ny)
# dx, dy = cellSize, cellSize
# xUV, yUV = dx * (range_x - 0.5*Nx), dy * (range_y - 0.5*Ny)

# dBeam_x, dBeam_y = np.pi/np.max(xUV), np.pi/np.max(yUV)
# Beam_xUV, Beam_yUV = dBeam_x * np.append(range_x[:Nx//2], -range_x[Nx//2:0:-1]), \
#                      dBeam_y * np.append(range_y[:Ny//2], -range_y[Ny//2:0:-1])

# x, y = np.meshgrid(xUV, yUV, sparse=False, indexing='ij')
# kx, ky = np.meshgrid(Beam_xUV, Beam_yUV, sparse=False, indexing='ij')

# # The sampling pattern, f = S(u, v)
# ax4 = fig.add_subplot(224, projection= '3d')
# ax4.set_title('$S(u, v)$ gridded')
# surf = ax4.plot_surface(x, y, np.abs(f), cmap= 'binary')

# # The dirty beam, F = B(l, m)
# ax3 = fig.add_subplot(223, projection= '3d')
# # https://stackoverflow.com/questions/11448972/
# ax3.xaxis.pane.fill = False
# ax3.yaxis.pane.fill = False
# ax3.zaxis.pane.fill = False

# # https://stackoverflow.com/questions/59857203/
# ax3.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
# ax3.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# ax3.grid(False)
# ax3.set_title('$B(\\ell , m)$')
# ax3.axes.get_xaxis().set_ticks([])
# ax3.axes.get_yaxis().set_ticks([])
# ax3.axes.get_zaxis().set_ticks([])

# surf = ax3.plot_surface(kx, ky, np.abs(F)*dx*dy, cmap= 'binary')

# plt.show()
# #=====================================================================
