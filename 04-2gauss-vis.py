#! /usr/bin/env python2.7

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Written by Vasaant S/O Krishnan on Saturday, 18 May 2019

# 04-gauss-vis.py "Gaussian visibility" plots aim to replicate figures from
# page 34 of "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the integrated source visibility, V(u) represented as a
# complex number. However instead of I(l) being a box function as in
# 04-box-vis.py, here I(l) is a Gaussian.





#=====================================================================
#     User variables
#
offset = 2             # Distance of source from origin
width  = 0.08          # Source width                         (dimensionless)

offsetTwo = -1         # Distance of second source from origin
widthTwo  = 0.1        # Second source's width                (dimensionless)

uLim   = 5             # Limit of range of baselines            (wavelengths)
steps  = 1000
#=====================================================================





#=====================================================================
#     Code begins here
#
u    = np.linspace(uLim, -uLim, steps)                 # Baseline span
uDeg = np.degrees(u)

lLim = 10                                              # Limit of range of source position (dimensionless)
lUpp =  lLim
lLow = -lLim
theta = np.linspace(lLow, lUpp, steps)

# Here I(l) is a Gaussian function for the range [lUpp, lLow]:
Iv = [np.exp(-np.power(l-   offset, 2)/(2*np.power(   width, 2))) for l in theta]
Iw = [np.exp(-np.power(l-offsetTwo, 2)/(2*np.power(widthTwo, 2))) for l in theta]
Ix = [a+b for a, b in zip(Iv, Iw)]

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u l)"  for all, l.
# cosr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
# sinr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]


cosr = [integrate.quad(lambda l: np.multiply(((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) + (1/np.sqrt(2*np.pi*np.power(widthTwo, 2.)))*np.exp(-np.power(l-offsetTwo, 2)/(2*np.power(widthTwo, 2)))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
sinr = [integrate.quad(lambda l: np.multiply(((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) + (1/np.sqrt(2*np.pi*np.power(widthTwo, 2.)))*np.exp(-np.power(l-offsetTwo, 2)/(2*np.power(widthTwo, 2)))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]


# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr, sinr)]     # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================





#=====================================================================
#     Plot
#
fig = plt.figure()

# Plot source, which is a Gaussian function
ax1 = fig.add_subplot(131)
ax1.plot(np.linspace(lLow,lUpp,steps), Ix)
ax1.set_xlim(-10,  10)
ax1.set_xticks(np.arange(-10, 11, 2))
ax1.set_ylim(  0, 1.05)
ax1.set_xlabel('Source width and offset')
ax1.set_title( 'Gaussian\n $\\frac{1}{\sqrt{2\\pi \\times %.2f}} \enspace e^{- \\frac{(\\ell - %.2f)^2}{2 \\times %.2f}}$'%(width, offset, width), y= 1.0)

# Plot the visibility cosine and sine components
ax2 = fig.add_subplot(132)
ax3 = ax2.twiny()
ax2.plot(   u, cosr, color= 'r')
ax3.plot(uDeg, sinr, color= 'b')
ax2.set_xlabel('Baseline (Spatial frequency)')
ax3.set_xlabel('(degrees)')
# ax2.set_ylim(-1.1, 1.1)
ax2.set_title( 'V(u): R$_c$ (r) and R$_s$ (b)', y= 1.09)

# Plot the visibility amplitude and phase
ax4 = fig.add_subplot(133)
ax5 = ax4.twiny()

ax4.plot(   u, amp, color= 'r')
ax5.plot(uDeg, pha, color= 'b')
ax4.set_xlabel('Baseline (Spatial frequency)')
ax4.set_title( 'V(u): Amp (r) and Phas (b)', y= 1.09)
ax4.set_xlim([-uLim, uLim])
if offset == 0:
    ax4.set_ylim(-0.1, 1.1)

plt.show()
