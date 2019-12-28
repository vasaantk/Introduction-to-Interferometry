#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Written by Vasaant S/O Krishnan on Saturday, 03 February 2018

# 02-vis-plot.py "visibility plot" replicates figures from page 31 of
# "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the complex visibilty function from the correlator in
# cosine and sine components.





#=====================================================================
#     User variables
#
u             = 3           # Baseline length                             (wavelengths)
field_of_view = 180         # Total range of field of view centred on zero    (degrees)
steps         = 10000
textsize      = 14
#=====================================================================





#=====================================================================
#     Code begins here
#
fov    = field_of_view/2.0                     # FOV centred on zero (see plot for zero)
rfov   = np.radians(fov)

xaxis  = np.linspace( fov,  -fov, steps)       # Top axis in degrees
theta  = np.linspace(rfov, -rfov, steps)       # Angular offset from perpendicular plane (radians)

l      = np.sin(theta)                         # Directional cosine ("ell") towards source, s

cosr   = np.cos(2 * np.pi * u * l)             # Interferometer cosine response, R_c
sinr   = np.sin(2 * np.pi * u * l)             # Interferometer sine   response, R_s

source = np.exp(-theta**2)                     # Gaussian brightness distribution, I_v(s)

cosEnv = [i*j for i, j in zip(source, cosr)]   # I_v(s) * cos
sinEnv = [i*j for i, j in zip(source, sinr)]   # I_v(s) * sin
#=====================================================================





#=====================================================================
#     Plotting
#
fig = plt.figure(figsize=(10, 8))

#==================================
#    Cosine plot params
ax1 = fig.add_subplot(121)
ax2 = ax1.twiny()                # Create twin 'x' axis to show radians and degrees

ax1.plot(theta, cosEnv)          # Plot [I_v(s) * cos] and give x-axis radians
ax2.plot(xaxis, source)          # Plot [I_v(s)]       and give x-axis degrees

cosInt = Polygon(zip(theta, cosEnv), facecolor='g', edgecolor='g')    # Integrated region of I_v(s) * cos
ax1.add_patch(cosInt)

ax1.set_title( 'I$_v$($\\ell $) * cos(2$\pi $ * ' + str(int(u)) + ' * $\\ell $)', y = 1.09, fontsize= textsize)
ax1.set_ylabel('Response from correlator (Left:  R$_c$ , Right:  R$_s$)', fontsize= textsize)
ax1.set_xlabel('Angular offset from perpendicular plane (radians)', fontsize= textsize)
ax2.set_xlabel('(degrees)', fontsize= textsize)
ax1.tick_params(axis='both', which='both', labelsize= textsize)
ax2.tick_params(axis='both', which='both', labelsize= textsize)

#==================================
#    Sine plot params
ax3 = fig.add_subplot(122)
ax4 = ax3.twiny()                # Create twin 'x' axis to show radians and degrees

ax3.plot(theta, sinEnv)          # Plot   I_v(s) * sin   with x-axis in radians
ax4.plot(xaxis, source)          # Plot   I_v(s)]        with x-axis in degrees

sinInt = Polygon(zip(theta,sinEnv), facecolor='g', edgecolor='g')    # Integrated region of I_v(s) * sin
ax3.add_patch(sinInt)

ax4.set_title('I$_v$($\\ell $) * sin(2$\pi $ * ' + str(int(u)) + ' * $\\ell $)', y = 1.09, fontsize= textsize)
ax3.tick_params(axis='both', which='both', labelsize= textsize)
ax4.tick_params(axis='both', which='both', labelsize= textsize)
ax3.get_yaxis().set_ticklabels([])

plt.savefig('02-vis-plot.eps', transparent=True, format='eps')
# plt.show()
