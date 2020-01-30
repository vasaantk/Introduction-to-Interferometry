#! /usr/bin/env python2.7

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Written by Vasaant S/O Krishnan on Tuesday, 06 March 2018

# 04-box-vis.py "box visibility" plots aim to replicate figures from
# page 34 of "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the integrated source visibility, V(u) represented as a
# complex number, when I(l) is a box function.
#
# As of Tuesday, 06 March 2018, 16:12 pm I have not been able to
# perfectly replicate the images in the slides. And do not have as
# much of an "intuitive" feel for the function V(u) as I would like.
#
# As of Wednesday, 01 August 2018, 17:56 I've managed to better
# replicate the slide images in a way which makes sense. It looks like
# "i/(np.pi/2)" in the Real and Imag components is needed to represent
# the baselines in units of radians of pi. However, it is bizarre that
# this factor should be different to that used in dirac-vis.py. Work
# needs to be done on the sine component of V(u).
#
# As of Monday, 08 April 2019, 16:47 PM I've corrected the
# "i/(np.pi/2)" to "i/np.pi", which is now consistent with
# dirac-vis.py. I've also made the source position ticks more user
# friendly. Work needs to be done on the sine component of V(u).
#
# As of Thursday, 11 April 2019, 13:07 PM. Previously, in
# 04-box-vis.py, I had been having difficulty in getting the sine
# component of V(u) to replicate what I found in in page 34 of "00
# Fundamentals of Radio Interferometry 1 - Perley.pdf" by using
# np.angle to automatically compute the phase angle. However, I was
# able to replicate the phases for 04-box-vis.py by manually computing
# amp = sqrt(cos**2 + sin**2) and phase = arctan(sin/cos). From my
# understanding, the former is the more robust (and correct?) method,
# though I will stick with the latter for now.
#
# As of Saturday, 18 May 2019, 06:36 am I have changed
# np.cos(2 * np.pi * k/np.pi * l)
# to
# np.cos(2 * np.pi * k * l/np.pi)
# from when the former was implemented on Wednesday, 01 August 2018,
# 14:41 pm in 03-dirac-vis.py. I think it makes sense as l is supposed
# to be the angular source position. and by dividing by pi, we represent it
# it in units of radians instead of an arbitrary number.





#=====================================================================
#     User variables
#
offset = 1           # Distance of source from origin
width  = 2           # Source width                (dimensionless)
ulim   = 5           # Limit of range of baselines   (wavelengths)
steps  = 10000
#=====================================================================





#=====================================================================
#     Code begins here
#
u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)

lUpp =  width/2. + offset
lLow = -width/2. + offset
l    = np.linspace(lUpp,  lLow, steps)

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the box function for the range [lUpp, lLow]:
cosr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.cos(2 * np.pi * k * l/np.pi), lLow, lUpp)[0] for k in u]    # Real component
sinr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.sin(2 * np.pi * k * l/np.pi), lLow, lUpp)[0] for k in u]    # Imag component

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

# Plot source, which is a box function
ax1 = fig.add_subplot(131)
ax1.fill_between(l, np.ones(len(l)), np.zeros(len(l)), color='black')
ax1.set_xlim(-10,  10)
ax1.set_xticks(np.arange(-10, 11, 2))
ax1.set_ylim(  0, 1.05)
ax1.set_xlabel('Source position and offset')
ax1.set_title( 'Box', y=1.09)

# Plot the visibility cosine and sine components
ax2 = fig.add_subplot(132)
ax3 = ax2.twiny()
ax2.plot(   u, cosr, color = 'r')
ax3.plot(uDeg, sinr, color = 'b')
ax2.set_xlabel('Baseline (Spatial frequency)')
ax3.set_xlabel('(degrees)')
ax2.set_ylim(-1.1, 1.1)
ax2.set_title( 'V(u): R$_c$ (r) and R$_s$ (b)', y=1.09)

# Plot the visibility amplitude and phase
ax4 = fig.add_subplot(133)
ax5 = ax4.twiny()

ax4.plot(   u, amp, color = 'r')
ax5.plot(uDeg, pha, color = 'b')
ax4.set_xlabel('Baseline (Spatial frequency)')
ax4.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09)
ax4.set_xlim([-ulim, ulim])
if offset == 0:
    ax4.set_ylim(-0.1, 1.1)

plt.show()
