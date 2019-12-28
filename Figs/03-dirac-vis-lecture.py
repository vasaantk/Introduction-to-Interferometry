#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Written by Vasaant S/O Krishnan on Tuesday, 06 March 2018

# 03-dirac-vis.py "dirac visibility" plots aim to replicates figures from
# page 33 of "00 Fundamentals of Radio Interferometry 1 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the integrated source visibility, V(u) represented as a
# complex number, when I(l) is a dirac delta function.

# As of Tuesday, 06 March 2018, 16:12 pm I have not been able to
# perfectly replicate the images in the slides. And do not have as
# much of an "intuitive" feel for the function V(u) as I would like.

# As of Wednesday, 01 August 2018, 14:41 pm I've managed to replicate
# the slide images in a way which makes sense. It looks like "i/np.pi"
# in the Real and Imag components is needed to represent the baselines
# in units of radians of pi. And do not have as much of an "intuitive"
# feel for the function V(u) as I would like.

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





#=====================================================================
#     User variables
#
l     = 0           # Source position             (dimensionless)
ulim  = 2           # Limit of range of baselines   (wavelengths)
steps = 10000
textsize = 13
#=====================================================================





# #=====================================================================
# #     Code begins here
# #
# u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
# uDeg = np.degrees(u)

# cosr = [np.cos(2 * np.pi * k/np.pi * l) for k in u]    # Real component
# sinr = [np.sin(2 * np.pi * k/np.pi * l) for k in u]    # Imag component

# # These compute the amp and phase manually:
# amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
# pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# # pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# # These use the numpy's built in functions instead:
# # vis  = [complex(i,j) for i,j in zip(cosr,sinr)]      # Visibility, V(u)
# # amp  = [   np.abs(i) for i in vis]
# # pha  = [ np.angle(i) for i in vis]
# #=====================================================================





#=====================================================================
#     Plot
#
fig = plt.figure(figsize=(10, 12))
plt.subplots_adjust(hspace= 0.5, wspace= 0.3)


# Plot source, which is a Dirac delta function

# 1st row
#=====================================================================
#     Code begins here
#
u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)
l    = l

cosr = [np.cos(2 * np.pi * k/np.pi * l) for k in u]    # Real component
sinr = [np.sin(2 * np.pi * k/np.pi * l) for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr,sinr)]      # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax1 = fig.add_subplot(331)
ax1.arrow(l, 0, 0, 0.95,
           head_width = 0.50,
          head_length = 0.05,
                   fc = 'k',
                   ec = 'k')
ax1.set_xlim(-10,  10)
ax1.set_xticks(np.arange(-10, 11, 4))
ax1.set_ylim([0, 1.06])
ax1.set_xlabel('Source position', fontsize= textsize)
ax1.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)

# Plot the visibility cosine and sine components
ax2 = fig.add_subplot(332)
ax3 = ax2.twiny()

ax2.plot(   u, cosr, color = 'r')
ax3.plot(uDeg, sinr, color = 'b')
ax2.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
ax3.set_xlabel('(degrees)', fontsize= textsize)
# ax2.set_title( '$\\mathcal{V}$(u): Real (red) and Imag (blue)\n', y=1.11, fontsize= textsize)
ax2.set_title( '$\mathcal{V}(u) = \int \\delta(\\ell - \\ell _0) \, e^{-i \, 2\\pi \, u \, \\ell } \, d\,\\ell \, = \, e^{-i \, 2\\pi \, u \, \\ell_0}$\n Real (red) and Imag (blue)\n', y=1.11, fontsize= textsize)
ax2.set_xlim([-ulim, ulim])
ax2.set_ylim(-1.1, 1.1)
ax1.tick_params(axis='both', which='both', labelsize= textsize)
ax2.tick_params(axis='both', which='both', labelsize= textsize)
ax3.tick_params(axis='both', which='both', labelsize= textsize)

# Plot the visibility amplitude and phase
ax4 = fig.add_subplot(333)
ax5 = ax4.twiny()

ax4.plot(   u, amp, color = 'r')
ax5.plot(uDeg, pha, color = 'b')
ax4.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
ax4.set_title( 'Amp (red) and Phas (blue)\n', y=1.10, fontsize= textsize)
ax5.set_xlabel('(degrees)', fontsize= textsize)
ax4.set_xlim([-ulim, ulim])
if l == 0:
    ax4.set_ylim(-0.1, 1.1)
ax1.tick_params(axis='both', which='both', labelsize= textsize)
ax2.tick_params(axis='both', which='both', labelsize= textsize)
ax3.tick_params(axis='both', which='both', labelsize= textsize)
ax4.tick_params(axis='both', which='both', labelsize= textsize)
ax5.tick_params(axis='both', which='both', labelsize= textsize)



# 2nd row
#=====================================================================
#     Code begins here
#
u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)
l    = l+2

cosr = [np.cos(2 * np.pi * k/np.pi * l) for k in u]    # Real component
sinr = [np.sin(2 * np.pi * k/np.pi * l) for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr,sinr)]      # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax6 = fig.add_subplot(334)
ax6.arrow(l, 0, 0, 0.95,
           head_width = 0.50,
          head_length = 0.05,
                   fc = 'k',
                   ec = 'k')
ax6.set_xlim(-10,  10)
ax6.set_xticks(np.arange(-10, 11, 4))
ax6.set_ylim([0, 1.06])
# ax6.set_xlabel('Source position', fontsize= textsize)
ax6.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)

# Plot the visibility cosine and sine components
ax7 = fig.add_subplot(335)
ax8 = ax7.twiny()

ax7.plot(   u, cosr, color = 'r')
ax8.plot(uDeg, sinr, color = 'b')
# ax7.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax8.set_xlabel('(degrees)', fontsize= textsize)
# ax7.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax7.set_xlim([-ulim, ulim])
ax7.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax9 = fig.add_subplot(336)
ax10 = ax9.twiny()

ax9.plot(   u, amp, color = 'r')
ax10.plot(uDeg, pha, color = 'b')
# ax9.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax9.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax9.set_xlim([-ulim, ulim])
if l == 0:
    ax9.set_ylim(-0.1, 1.1)
ax6.tick_params(axis='both', which='both', labelsize= textsize)
ax7.tick_params(axis='both', which='both', labelsize= textsize)
ax8.tick_params(axis='both', which='both', labelsize= textsize)
ax9.tick_params(axis='both', which='both', labelsize= textsize)
ax10.tick_params(axis='both', which='both', labelsize= textsize)



# 3rd row
#=====================================================================
#     Code begins here
#
u    = np.linspace(ulim, -ulim, steps)                 # Baseline span
uDeg = np.degrees(u)
l    = l+5

cosr = [np.cos(2 * np.pi * k/np.pi * l) for k in u]    # Real component
sinr = [np.sin(2 * np.pi * k/np.pi * l) for k in u]    # Imag component

# These compute the amp and phase manually:
amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# These use the numpy's built in functions instead:
# vis  = [complex(i,j) for i,j in zip(cosr,sinr)]      # Visibility, V(u)
# amp  = [   np.abs(i) for i in vis]
# pha  = [ np.angle(i) for i in vis]
#=====================================================================

ax11 = fig.add_subplot(337)
ax11.arrow(l, 0, 0, 0.95,
           head_width = 0.50,
          head_length = 0.05,
                   fc = 'k',
                   ec = 'k')
ax11.set_xlim(-10,  10)
ax11.set_xticks(np.arange(-10, 11, 4))
ax11.set_ylim([0, 1.06])
# ax11.set_xlabel('Source position', fontsize= textsize)
ax11.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)

# Plot the visibility cosine and sine components
ax12 = fig.add_subplot(338)
ax13 = ax12.twiny()

ax12.plot(   u, cosr, color = 'r')
ax13.plot(uDeg, sinr, color = 'b')
# ax12.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax13.set_xlabel('(degrees)', fontsize= textsize)
# ax12.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax12.set_xlim([-ulim, ulim])
ax12.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax14 = fig.add_subplot(339)
ax15 = ax14.twiny()

ax14.plot(   u, amp, color = 'r')
ax15.plot(uDeg, pha, color = 'b')
# ax14.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax14.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax14.set_xlim([-ulim, ulim])
if l == 0:
    ax14.set_ylim(-0.1, 1.1)
ax11.tick_params(axis='both', which='both', labelsize= textsize)
ax12.tick_params(axis='both', which='both', labelsize= textsize)
ax13.tick_params(axis='both', which='both', labelsize= textsize)
ax14.tick_params(axis='both', which='both', labelsize= textsize)
ax15.tick_params(axis='both', which='both', labelsize= textsize)

# plt.savefig('03-dirac-vis.eps', transparent=True, format='eps')
plt.show()
