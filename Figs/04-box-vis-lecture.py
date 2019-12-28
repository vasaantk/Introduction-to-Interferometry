#! /usr/bin/env python2.7

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Written by Vasaant S/O Krishnan on Tuesday, 06 March 2018

# 04-box-vis.py "box visibility" plots aim to replicates figures from
# page 34 of "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the integrated source visibility, V(u) represented as a
# complex number, when I(l) is a box function.

# As of Tuesday, 06 March 2018, 16:12 pm I have not been able to
# perfectly replicate the images in the slides. And do not have as
# much of an "intuitive" feel for the function V(u) as I would like.

# As of Wednesday, 01 August 2018, 17:56 I've managed to better
# replicate the slide images in a way which makes sense. It looks like
# "i/(np.pi/2)" in the Real and Imag components is needed to represent
# the baselines in units of radians of pi. However, it is bizarre that
# this factor should be different to that used in dirac-vis.py. Work
# needs to be done on the sine component of V(u).

# As of Monday, 08 April 2019, 16:47 PM I've corrected the
# "i/(np.pi/2)" to "i/np.pi", which is now consistent with
# dirac-vis.py. I've also made the source position ticks more user
# friendly. Work needs to be done on the sine component of V(u).

# As of Thursday, 11 April 2019, 13:07 PM. Previously, in
# 04-box-vis.py, I had been having difficulty in getting the sine
# component of V(u) to replicate what I found in in page 34 of "00
# Fundamentals of Radio Interferometry 1 - Perley.pdf" by using
# np.angle to automatically compute the phase angle. However, I was
# able to replicate the phases for 04-box-vis.py by manually computing
# amp = sqrt(cos**2 + sin**2) and phase = arctan(sin/cos). From my
# understanding, the former is the more robust (and correct?) method,
# though I will stick with the latter for now.





#=====================================================================
#     User variables
#
ulim  = 5           # Limit of range of baselines   (wavelengths)
steps = 10000
textsize = 13
#=====================================================================





#=====================================================================
#     Plot
#
fig = plt.figure(figsize=(10, 12))
plt.subplots_adjust(hspace= 0.6, wspace= 0.5)


# Plot source, which is a box function

# 1st row
#=====================================================================
#     Code begins here
#
offset = 0           # Distance of source from origin
width  = 2           # Source width                (dimensionless)

u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)

lUpp =  width/2. + offset
lLow = -width/2. + offset
l    = np.linspace(lUpp,  lLow, steps)

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the box function for the range [lUpp, lLow]:
cosr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.cos(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Real component
sinr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.sin(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr, sinr)]     # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax1 = fig.add_subplot(4,3,1)
ax1.fill_between(l, np.ones(len(l)), np.zeros(len(l)), color='black')
ax1.set_xlim(-10,  10)
ax1.set_xticks(np.arange(-10, 11, 4))
ax1.set_ylim([0, 1.06])
ax1.set_xlabel('Source width and offset', fontsize= textsize)
ax1.set_title( 'Box', y=1.09)

# Plot the visibility cosine and sine components
ax2 = fig.add_subplot(4,3,2)
ax3 = ax2.twiny()

ax2.plot(   u, cosr, color = 'r')
ax3.plot(uDeg, sinr, color = 'b')
ax2.set_xlabel('Baseline (Spatial frequency)', fontsize= 11)
ax3.set_xlabel('(degrees)', fontsize= 11)
# ax2.set_title( '$\\mathcal{V}$(u): Real (red) and Imag (blue)\n', y=1.11, fontsize= textsize)
ax2.set_title( '$\mathcal{V}(u) = \int I_\\nu (\\ell )\, e^{-i \, 2\\pi \, u \, \\ell } \, d\,\\ell}$\n Real (red) and Imag (blue)\n', y=1.11, fontsize= textsize)
ax2.set_xlim([-ulim, ulim])
ax2.set_ylim(-1.1, 1.1)
ax1.tick_params(axis='both', which='both', labelsize= textsize)
ax2.tick_params(axis='both', which='both', labelsize= textsize)
ax3.tick_params(axis='both', which='both', labelsize= textsize)

# Plot the visibility amplitude and phase
ax4 = fig.add_subplot(4,3,3)
ax5 = ax4.twiny()

ax4.plot(   u, amp, color = 'r')
ax5.plot(uDeg, pha, color = 'b')
# ax4.set_xlabel('Baseline (Spatial frequency)', fontsize= textsize)
ax4.set_title( 'Amp (red) and Phas (blue)\n', y=1.10, fontsize= textsize)
# ax5.set_xlabel('(degrees)', fontsize= textsize)
ax4.set_xlim([-ulim, ulim])
ax1.tick_params(axis='both', which='both', labelsize= textsize)
ax2.tick_params(axis='both', which='both', labelsize= textsize)
ax3.tick_params(axis='both', which='both', labelsize= textsize)
ax4.tick_params(axis='both', which='both', labelsize= textsize)
ax5.tick_params(axis='both', which='both', labelsize= textsize)



# 2nd row
#=====================================================================
#     Code begins here
#
offset = 0           # Distance of source from origin
width  = 6           # Source width                (dimensionless)

u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)

lUpp =  width/2. + offset
lLow = -width/2. + offset
l    = np.linspace(lUpp,  lLow, steps)

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the box function for the range [lUpp, lLow]:
cosr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.cos(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Real component
sinr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.sin(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr, sinr)]     # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax6 = fig.add_subplot(4,3,4)
ax6.fill_between(l, np.ones(len(l)), np.zeros(len(l)), color='black')
ax6.set_xlim(-10,  10)
ax6.set_xticks(np.arange(-10, 11, 4))
ax6.set_ylim([0, 1.06])
# ax6.set_xlabel('Source position', fontsize= textsize)
# ax6.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)

# Plot the visibility cosine and sine components
ax7 = fig.add_subplot(4,3,5)
ax8 = ax7.twiny()

ax7.plot(   u, cosr, color = 'r')
ax8.plot(uDeg, sinr, color = 'b')
# ax7.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax8.set_xlabel('(degrees)', fontsize= textsize)
# ax7.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax7.set_xlim([-ulim, ulim])
ax7.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax9 = fig.add_subplot(4,3,6)
ax10 = ax9.twiny()

ax9.plot(   u, amp, color = 'r')
ax10.plot(uDeg, pha, color = 'b')
# ax9.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax9.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax9.set_xlim([-ulim, ulim])
ax6.tick_params(axis='both', which='both', labelsize= textsize)
ax7.tick_params(axis='both', which='both', labelsize= textsize)
ax8.tick_params(axis='both', which='both', labelsize= textsize)
ax9.tick_params(axis='both', which='both', labelsize= textsize)
ax10.tick_params(axis='both', which='both', labelsize= textsize)



# 3rd row
#=====================================================================
#     Code begins here
#
offset = 3           # Distance of source from origin
width  = 2           # Source width                (dimensionless)

u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)

lUpp =  width/2. + offset
lLow = -width/2. + offset
l    = np.linspace(lUpp,  lLow, steps)

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the box function for the range [lUpp, lLow]:
cosr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.cos(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Real component
sinr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.sin(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr, sinr)]     # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax11 = fig.add_subplot(4,3,7)
ax11.fill_between(l, np.ones(len(l)), np.zeros(len(l)), color='black')
ax11.set_xlim(-10,  10)
ax11.set_xticks(np.arange(-10, 11, 4))
ax11.set_ylim([0, 1.06])
# ax11.set_xlabel('Source position', fontsize= textsize)
# ax11.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)

# Plot the visibility cosine and sine components
ax12 = fig.add_subplot(4,3,8)
ax13 = ax12.twiny()

ax12.plot(   u, cosr, color = 'r')
ax13.plot(uDeg, sinr, color = 'b')
# ax12.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax13.set_xlabel('(degrees)', fontsize= textsize)
# ax12.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax12.set_xlim([-ulim, ulim])
ax12.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax14 = fig.add_subplot(4,3,9)
ax15 = ax14.twiny()

ax14.plot(   u, amp, color = 'r')
ax15.plot(uDeg, pha, color = 'b')
# ax14.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax14.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax14.set_xlim([-ulim, ulim])
ax11.tick_params(axis='both', which='both', labelsize= textsize)
ax12.tick_params(axis='both', which='both', labelsize= textsize)
ax13.tick_params(axis='both', which='both', labelsize= textsize)
ax14.tick_params(axis='both', which='both', labelsize= textsize)
ax15.tick_params(axis='both', which='both', labelsize= textsize)



# 4th row
#=====================================================================
#     Code begins here
#
offset = -4           # Distance of source from origin
width  = 6           # Source width                (dimensionless)

u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)

lUpp =  width/2. + offset
lLow = -width/2. + offset
l    = np.linspace(lUpp,  lLow, steps)

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the box function for the range [lUpp, lLow]:
cosr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.cos(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Real component
sinr = [(1./(np.abs(lLow-lUpp))) * integrate.quad(lambda l: np.sin(2 * np.pi * k/np.pi * l), lLow, lUpp)[0] for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr, sinr)]     # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax16 = fig.add_subplot(4,3,10)
ax16.fill_between(l, np.ones(len(l)), np.zeros(len(l)), color='black')
ax16.set_xlim(-10,  10)
ax16.set_xticks(np.arange(-10, 11, 4))
ax16.set_ylim([0, 1.06])
# ax16.set_xlabel('Source position', fontsize= textsize)
# ax16.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)

# Plot the visibility cosine and sine components
ax17 = fig.add_subplot(4,3,11)
ax18 = ax17.twiny()

ax17.plot(   u, cosr, color = 'r')
ax18.plot(uDeg, sinr, color = 'b')
# ax17.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax18.set_xlabel('(degrees)', fontsize= textsize)
# ax17.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax17.set_xlim([-ulim, ulim])
ax17.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax19 = fig.add_subplot(4,3,12)
ax20 = ax19.twiny()

ax19.plot(   u, amp, color = 'r')
ax20.plot(uDeg, pha, color = 'b')
# ax19.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax19.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax19.set_xlim([-ulim, ulim])
ax16.tick_params(axis='both', which='both', labelsize= textsize)
ax17.tick_params(axis='both', which='both', labelsize= textsize)
ax18.tick_params(axis='both', which='both', labelsize= textsize)
ax19.tick_params(axis='both', which='both', labelsize= textsize)
ax20.tick_params(axis='both', which='both', labelsize= textsize)


plt.savefig('04-box-vis.eps', transparent=True, format='eps')
# plt.show()
