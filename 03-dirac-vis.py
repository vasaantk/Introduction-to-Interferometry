#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Written by Vasaant S/O Krishnan on Tuesday, 06 March 2018

# 03-dirac-vis.py "dirac visibility" plots aim to replicates figures from
# page 33 of "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the integrated source visibility, V(u) represented as a
# complex number, when I(l) is a dirac delta function.
#
# As of Tuesday, 06 March 2018, 16:12 pm I have not been able to
# perfectly replicate the images in the slides. And do not have as
# much of an "intuitive" feel for the function V(u) as I would like.
#
# As of Wednesday, 01 August 2018, 14:41 pm I've managed to replicate
# the slide images in a way which makes sense. It looks like "i/np.pi"
# in the Real and Imag components is needed to represent the baselines
# in units of radians of pi. And do not have as much of an "intuitive"
# feel for the function V(u) as I would like.
#
# As of Thursday, 11 April 2019, 13:07 PM I've made changes here which
# are based on 04-box-vis.py. Previously, in 04-box-vis.py, I had been
# having difficulty in getting the sine component of V(u) to replicate
# what I found in in page 34 of "00 Fundamentals of Radio
# Interferometry 1 - Perley.pdf" by using np.angle to automatically
# compute the phase angle. However, I was able to replicate the phases
# for 04-box-vis.py by manually computing amp = sqrt(cos**2 + sin**2)
# and phase = arctan(sin/cos). From my understanding, the former is
# the more robust (and correct?) method, though I will stick with the
# latter for now.
#
# As of Saturday, 18 May 2019, 06:36 am I have changed
# cosr = [np.cos(2 * np.pi * k/np.pi * l) for k in u]    # Real component
# to
# cosr = [np.cos(2 * np.pi * k * l/np.pi) for k in u]    # Real component
# from when the former was implemented on Wednesday, 01 August 2018,
# 14:41 pm in 03-dirac-vis.py. I think it makes sense as l is supposed
# to be the angular source position. and by dividing by pi, we represent it
# it in units of radians instead of an arbitrary number.




#=====================================================================
#     User variables
#
l     = 0           # Source position             (dimensionless)
ulim  = 5           # Limit of range of baselines   (wavelengths)
steps = 10000
#=====================================================================





#=====================================================================
#     Code begins here
#
u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)

cosr = [np.cos(2 * np.pi * k * l/np.pi) for k in u]    # Real component
sinr = [np.sin(2 * np.pi * k * l/np.pi) for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr,sinr)]      # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================





#=====================================================================
#     Plot
#
fig = plt.figure()

# Plot source, which is a Dirac delta function
ax1 = fig.add_subplot(131)
ax1.arrow(l, 0, 0, 0.95,
           head_width = 0.50,
          head_length = 0.05,
                   fc = 'k',
                   ec = 'k')
ax1.set_xlim(-10,  10)
ax1.set_xticks(np.arange(-10, 11, 2))
ax1.set_ylim([0, 1.06])
ax1.set_xlabel('Source position')
ax1.set_title( '$\\delta (\\ell - %d$)'%l)

# Plot the visibility cosine and sine components
ax2 = fig.add_subplot(132)
ax3 = ax2.twiny()

ax2.plot(   u, cosr, color = 'r')
ax3.plot(uDeg, sinr, color = 'b')
ax2.set_xlabel('Baseline (Spatial frequency)')
ax3.set_xlabel('(degrees)')
ax2.set_title( 'V(u): Real (r) and Imag (b)', y=1.09)
ax2.set_xlim([-ulim, ulim])
ax2.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax4 = fig.add_subplot(133)
ax5 = ax4.twiny()

ax4.plot(   u, amp, color = 'r')
ax5.plot(uDeg, pha, color = 'b')
ax4.set_xlabel('Baseline (Spatial frequency)')
ax4.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09)
ax4.set_xlim([-ulim, ulim])
if l == 0:
    ax4.set_ylim(-0.1, 1.1)

plt.show()
