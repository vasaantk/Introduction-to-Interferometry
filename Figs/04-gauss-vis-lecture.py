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
uLim   = 5             # Limit of range of baselines            (wavelengths)
steps  = 10000
textsize = 13
#=====================================================================





# #=====================================================================
# #     Code begins here
# #
# u    = np.linspace(uLim, -uLim, steps)                 # Baseline span
# uDeg = np.degrees(u)

# lLim = 10                                              # Limit of range of source position (dimensionless)
# lUpp =  lLim
# lLow = -lLim
# theta = np.linspace(lLow, lUpp, steps)

# # Here I(l) is a Gaussian function for the range [lUpp, lLow]:
# Iv = [np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) for l in theta]

# # For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u l)"  for all, l.
# cosr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
# sinr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]

# # These compute the amp and phase manually:
# amp = [np.sqrt(i**2 + j**2) for i, j in zip(cosr, sinr)]
# pha = [      np.arctan(j/i) for i, j in zip(cosr, sinr)]
# # pha = [     np.arctan2(j,i) for i, j in zip(cosr, sinr)]    # This is akin to using np.angle as below

# # These use the numpy's built in functions instead:
# # vis  = [complex(i,j) for i,j in zip(cosr, sinr)]     # Visibility, V(u)
# # amp  = [   np.abs(i) for i in vis]
# # pha  = [ np.angle(i) for i in vis]
# #=====================================================================





# #=====================================================================
# #     Plot
# #
# plt.subplots_adjust(hspace= 0.6, wspace= 0.5)
# fig = plt.figure()

# # Plot source, which is a Gaussian function
# ax1 = fig.add_subplot(131)
# ax1.plot(np.linspace(lLow,lUpp,steps), Iv)
# ax1.set_xlim(-10,  10)
# ax1.set_xticks(np.arange(-10, 11, 2))
# ax1.set_ylim(  0, 1.05)
# ax1.set_xlabel('Source width and offset')
# ax1.set_title( 'Gaussian\n $\\frac{1}{\sqrt{2\\pi \\times %.2f}} \enspace e^{- \\frac{(\\ell - %.2f)^2}{2 \\times %.2f}}$'%(width, offset, width), y= 1.0)

# # Plot the visibility cosine and sine components
# ax2 = fig.add_subplot(132)
# ax3 = ax2.twiny()
# ax2.plot(   u, cosr, color= 'r')
# ax3.plot(uDeg, sinr, color= 'b')
# ax2.set_xlabel('Baseline (Spatial frequency)')
# ax3.set_xlabel('(degrees)')
# ax2.set_ylim(-1.1, 1.1)
# ax2.set_title( 'V(u): R$_c$ (r) and R$_s$ (b)', y= 1.09)

# # Plot the visibility amplitude and phase
# ax4 = fig.add_subplot(133)
# ax5 = ax4.twiny()

# ax4.plot(   u, amp, color= 'r')
# ax5.plot(uDeg, pha, color= 'b')
# ax4.set_xlabel('Baseline (Spatial frequency)')
# ax4.set_title( 'V(u): Amp (r) and Phas (b)', y= 1.09)
# ax4.set_xlim([-uLim, uLim])
# if offset == 0:
#     ax4.set_ylim(-0.1, 1.1)

# plt.show()







#****
#=====================================================================
#     Plot
#
fig = plt.figure(figsize=(10, 12))
plt.subplots_adjust(hspace= 0.6, wspace= 0.5)


# Plot source, which is a Gaussian function

# 1st row
#=====================================================================
#     Code begins here
#
offset = 0           # Distance of source from origin
width  = 0.08        # Source width                (dimensionless)

u    = np.linspace(uLim, -uLim, steps)                 # Baseline span
uDeg = np.degrees(u)

lLim = 10                                              # Limit of range of source position (dimensionless)
lUpp =  lLim
lLow = -lLim
theta = np.linspace(lLow, lUpp, steps)

# Here I(l) is a Gaussian function for the range [lUpp, lLow]:
Iv = [np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) for l in theta]

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the Gaussian function for the range [lUpp, lLow]:
cosr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
sinr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]

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
ax1.plot(np.linspace(lLow,lUpp,steps), Iv)
ax1.set_xlim(-10,  10)
ax1.set_xticks(np.arange(-10, 11, 4))
ax1.set_ylim([0, 1.06])
ax1.set_xlabel('Source width and offset', fontsize= textsize)
# ax1.set_title( 'Gaussian', y=1.09)
ax1.set_title( '$\\frac{1}{\sqrt{2\\pi \\times %.2f}} \enspace e^{- \\frac{(\\ell - %.2f)^2}{2 \\times %.2f}}$'%(width, offset, width), y= 1.05)

# Plot the visibility cosine and sine components
ax2 = fig.add_subplot(4,3,2)
ax3 = ax2.twiny()

ax2.plot(   u, cosr, color = 'r')
ax3.plot(uDeg, sinr, color = 'b')
ax2.set_xlabel('Baseline (Spatial frequency)', fontsize= 11)
ax3.set_xlabel('(degrees)', fontsize= 11)
# ax2.set_title( '$\\mathcal{V}$(u): Real (red) and Imag (blue)\n', y=1.11, fontsize= textsize)
ax2.set_title( '$\mathcal{V}(u) = \int I_\\nu (\\ell )\, e^{-i \, 2\\pi \, u \, \\ell } \, d\,\\ell}$\n Real (red) and Imag (blue)\n', y=1.11, fontsize= textsize)
ax2.set_xlim([-uLim, uLim])
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
ax4.set_xlim([-uLim, uLim])
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
width  = 1.0         # Source width                (dimensionless)

u    = np.linspace(uLim, -uLim, steps)                 # Baseline span
uDeg = np.degrees(u)

lLim = 10                                              # Limit of range of source position (dimensionless)
lUpp =  lLim
lLow = -lLim
theta = np.linspace(lLow, lUpp, steps)

# Here I(l) is a Gaussian function for the range [lUpp, lLow]:
Iv = [np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) for l in theta]

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the Gaussian function for the range [lUpp, lLow]:
cosr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
sinr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]

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
ax6.plot(np.linspace(lLow,lUpp,steps), Iv)
ax6.set_xlim(-10,  10)
ax6.set_xticks(np.arange(-10, 11, 4))
ax6.set_ylim([0, 1.06])
# ax6.set_xlabel('Source position', fontsize= textsize)
ax6.set_title( '$\\frac{1}{\sqrt{2\\pi \\times %.2f}} \enspace e^{- \\frac{(\\ell - %.2f)^2}{2 \\times %.2f}}$'%(width, offset, width), y= 1.05)

# Plot the visibility cosine and sine components
ax7 = fig.add_subplot(4,3,5)
ax8 = ax7.twiny()

ax7.plot(   u, cosr, color = 'r')
ax8.plot(uDeg, sinr, color = 'b')
# ax7.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax8.set_xlabel('(degrees)', fontsize= textsize)
# ax7.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax7.set_xlim([-uLim, uLim])
ax7.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax9 = fig.add_subplot(4,3,6)
ax10 = ax9.twiny()

ax9.plot(   u, amp, color = 'r')
ax10.plot(uDeg, pha, color = 'b')
# ax9.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax9.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax9.set_xlim([-uLim, uLim])
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
width  = 0.08        # Source width                (dimensionless)

u    = np.linspace(uLim, -uLim, steps)                 # Baseline span
uDeg = np.degrees(u)

lLim = 10                                              # Limit of range of source position (dimensionless)
lUpp =  lLim
lLow = -lLim
theta = np.linspace(lLow, lUpp, steps)

# Here I(l) is a Gaussian function for the range [lUpp, lLow]:
Iv = [np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) for l in theta]

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the Gaussian function for the range [lUpp, lLow]:
cosr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
sinr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]

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
ax11.plot(np.linspace(lLow,lUpp,steps), Iv)
ax11.set_xlim(-10,  10)
ax11.set_xticks(np.arange(-10, 11, 4))
ax11.set_ylim([0, 1.06])
# ax11.set_xlabel('Source position', fontsize= textsize)
# ax11.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)
ax11.set_title( '$\\frac{1}{\sqrt{2\\pi \\times %.2f}} \enspace e^{- \\frac{(\\ell - %.2f)^2}{2 \\times %.2f}}$'%(width, offset, width), y= 1.05)

# Plot the visibility cosine and sine components
ax12 = fig.add_subplot(4,3,8)
ax13 = ax12.twiny()

ax12.plot(   u, cosr, color = 'r')
ax13.plot(uDeg, sinr, color = 'b')
# ax12.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax13.set_xlabel('(degrees)', fontsize= textsize)
# ax12.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax12.set_xlim([-uLim, uLim])
ax12.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax14 = fig.add_subplot(4,3,9)
ax15 = ax14.twiny()

ax14.plot(   u, amp, color = 'r')
ax15.plot(uDeg, pha, color = 'b')
# ax14.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax14.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax14.set_xlim([-uLim, uLim])
ax11.tick_params(axis='both', which='both', labelsize= textsize)
ax12.tick_params(axis='both', which='both', labelsize= textsize)
ax13.tick_params(axis='both', which='both', labelsize= textsize)
ax14.tick_params(axis='both', which='both', labelsize= textsize)
ax15.tick_params(axis='both', which='both', labelsize= textsize)



# 4th row
#=====================================================================
#     Code begins here
#
offset = -1.5           # Distance of source from origin
width  = 0.15          # Source width                (dimensionless)

u    = np.linspace(uLim, -uLim, steps)                 # Baseline span
uDeg = np.degrees(u)

lLim = 10                                              # Limit of range of source position (dimensionless)
lUpp =  lLim
lLow = -lLim
theta = np.linspace(lLow, lUpp, steps)

# Here I(l) is a Gaussian function for the range [lUpp, lLow]:
Iv = [np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))) for l in theta]

# For each baseline, u, integrate "Re[V(u)] = I(l)*cos(2pi u  l)"  for all, l.
# Here I(l) is the Gaussian function for the range [lUpp, lLow]:
cosr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.cos(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]
sinr = [integrate.quad(lambda l: np.multiply((1/np.sqrt(2*np.pi*np.power(width, 2.)))*np.exp(-np.power(l-offset, 2)/(2*np.power(width, 2))), np.sin(2 * np.pi * k * l/np.pi)), theta[0], theta[-1])[0] for k in u]

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
ax16.plot(np.linspace(lLow,lUpp,steps), Iv)
ax16.set_xlim(-10,  10)
ax16.set_xticks(np.arange(-10, 11, 4))
ax16.set_ylim([0, 1.06])
# ax16.set_xlabel('Source position', fontsize= textsize)
# ax16.set_title( '$\\delta (\\ell - %d$)'%l, fontsize= textsize)
ax16.set_title( '$\\frac{1}{\sqrt{2\\pi \\times %.2f}} \enspace e^{- \\frac{(\\ell + %.2f)^2}{2 \\times %.2f}}$'%(width, abs(offset), width), y= 1.05)

# Plot the visibility cosine and sine components
ax17 = fig.add_subplot(4,3,11)
ax18 = ax17.twiny()

ax17.plot(   u, cosr, color = 'r')
ax18.plot(uDeg, sinr, color = 'b')
# ax17.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax18.set_xlabel('(degrees)', fontsize= textsize)
# ax17.set_title( 'V(u): Real (r) and Imag (b)', y=1.09, fontsize= textsize)
ax17.set_xlim([-uLim, uLim])
ax17.set_ylim(-1.1, 1.1)

# Plot the visibility amplitude and phase
ax19 = fig.add_subplot(4,3,12)
ax20 = ax19.twiny()

ax19.plot(   u, amp, color = 'r')
ax20.plot(uDeg, pha, color = 'b')
# ax19.set_xlabel('Baseline\n (Spatial frequency)', fontsize= textsize)
# ax19.set_title( 'V(u): Amp (r) and Phas (b)', y=1.09, fontsize= textsize)
ax19.set_xlim([-uLim, uLim])
ax16.tick_params(axis='both', which='both', labelsize= textsize)
ax17.tick_params(axis='both', which='both', labelsize= textsize)
ax18.tick_params(axis='both', which='both', labelsize= textsize)
ax19.tick_params(axis='both', which='both', labelsize= textsize)
ax20.tick_params(axis='both', which='both', labelsize= textsize)


# plt.savefig('04-gauss-vis.eps', transparent=True, format='eps')
plt.show()
