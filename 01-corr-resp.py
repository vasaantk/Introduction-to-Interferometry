#! /usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Written by Vasaant S/O Krishnan on Tuesday, 30 January 2018

# 01-corr-resp.py ("correlator response") plots "R_c = P*cos(2pi u l)"
# from page 15 - 17 of "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# It also prints out the maxiama and minima of the fringes.

# As of Monday, 08 April 2019, 15:40 PM I've made an important
# correction by removing the abs(i) for 'cycl' and 'resp', which seems
# to be the correct thing to do. Now the number of fringes are
# consistent with 'rect'. I cannot get the polar plot axis range to
# span [-180, 180] degrees yet.

# Usage:
#   -->$ 01-corr-resp.py option

#   where 'option' can be:
#
#       rect  = plot in cartesian coordinates
#       cycl  = plot in polar coordinates
#       resp  = plot with customised receiver response
#       print = output maxima and minima to terminal





#=====================================================================
#     User variables
#
u             = 3           # Baseline length                             (wavelengths)
field_of_view = 180         # Total range of field of view centred on zero    (degrees)
steps         = 10000
#=====================================================================





#=====================================================================
#     Code begins here
#
usrInp = sys.argv[1:]

fov   = field_of_view/2.0                  # FOV centred on zero (see plot for zero)
rfov  = np.radians(fov)

xaxis = np.linspace( fov,  -fov, steps)    # Top axis in degrees
theta = np.linspace(rfov, -rfov, steps)    # Angular offset from perpendicular plane (radians)

l     = np.sin(theta)                      # Directional cosine ("ell") towards source, s
cosr  = np.cos(2 * np.pi * u * l)          # Interferometer cosine response, R_c
#=====================================================================





#=====================================================================
#     Print maxima/minima for which "R_c = P*cos(2pi u l)" is 1 or -1
#     Look at the bottom of page 4 of my personal notes for details.
#
if 'print' in usrInp:
    print "%5s  %6s  %6s"%('n', 'rad', 'deg')
    print ""
    firstPass = True
    for i in range(-u, u+1):

        i = float(i)
        u = float(u)

        if firstPass:                  # Print "max" , "min" fin the first instance
            maxima = np.arcsin(i/u)    # Values of Theta where R_c is max
            print "%5d  %6.2f  %6.2f         max"%(i, maxima, np.degrees(maxima))
            if i < u:
                minima = np.arcsin((2*i+1)/(2*u))    # Values of Theta where R_c is min
                print "%10s  %6.2f  %6.2f    min"%(" ", minima, np.degrees(minima))
            firstPass = False
        else:
            maxima = np.arcsin(i/u)
            print "%5d  %6.2f  %6.2f           "%(i, maxima, np.degrees(maxima))
            if i < u:
                minima = np.arcsin((2*i+1)/(2*u))    # Values of Theta where R_c is min
                print "%10s  %6.2f  %6.2f      "%(" ", minima, np.degrees(minima))
#=====================================================================





#=====================================================================
#     Plotting
#
if 'rect' in usrInp:
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()                # Create twin 'x' axis to show radians and degrees

    ax1.plot(theta, cosr)
    ax2.plot(xaxis, cosr)            # Top axis in degrees

    plt.suptitle('R$_c$ = cos(2$\pi $ * ' + str(int(u)) + ' * $\ell$)')
    ax1.set_ylabel('Response from correlator (R$_c$)')
    ax1.set_xlabel('Angular offset from perpendicular plane (radians)')
    ax2.set_xlabel('(degrees)')

    plt.show()




if 'cycl' in usrInp:
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection = 'polar')

    ax1.plot(theta, cosr)

    plt.suptitle('R$_c$ = cos(2$\pi $ * ' + str(int(u)) + ' * $\ell$)')
    ax1.set_theta_offset(np.pi/2)
    ax1.set_theta_direction(-1)
    ax1.set_thetamin(-fov)
    ax1.set_thetamax( fov)
    # tickLabs = [0, 45, 90, 135, 180, -135, -90, -45]
    # plt.xticks(ax1.get_xticks(), tickLabs)
    ax1.set_aspect('equal')
    ax1.set_rticks([])

    plt.show()




if 'resp' in usrInp:

    def gaussian(x, mu, sig):
        return np.exp(-np.power(x-mu, 2.)/(2*np.power(sig, 2.)))

    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection = 'polar')

    # receiver = np.cos(theta)                          # Cosine response function of receiver
    receiver = gaussian(theta, 0, 0.1)                  # Gaussian response function of receiver
    rec_cosr = [i*j for i, j in zip(receiver, cosr)]    # Receiver * Response

    ax1.plot(theta, np.abs(rec_cosr))

    plt.suptitle('R$_c$ = cos(2$\pi $ * ' + str(int(u)) + ' * $\ell$)')
    ax1.set_theta_offset(np.pi/2)
    ax1.set_theta_direction(-1)
    # ax1.set_xticks(np.pi/180. * np.linspace(-180, 180, 8, endpoint=False))
    ax1.set_aspect('equal')
    ax1.set_rticks([])

    plt.show()




if 'thre' in usrInp:

    # As of Wednesday, 31 January 2018, I cannot get the 3D plot to
    # work.

    fig = plt.figure()
    ax  = fig.add_subplot(111, projection = '3d')

    x = theta
    y = cosr

    r = [np.sqrt(i**2 + j**2) for i, j in zip(x, y)]
    p = [np.arctan(abs(j/i))  for i, j in zip(x, y)]

    R, P = np.meshgrid(r,p)
    Z    = R

    X, Y = R*np.cos(P), R*np.sin(P)

    ax.plot_surface(X, Y, Z)
#=====================================================================
