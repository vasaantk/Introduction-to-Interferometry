#! /usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Written by Vasaant S/O Krishnan on Saturday, 28 July 2018, 15:53 pm
#
# 05-fin-band.py "Finite bandwidth" shows the effect of finite bandwidth
# from page 7 of "01 Fundamentals of Radio Interferometry 2 - Perley.pdf"
# https://science.nrao.edu/science/meetings/2015/summer-schools/interferometry-program
# Which is the complex visibilty function from the correlator in
# cosine and sine components multiplied by the sinc function as a
# result of a finite square bandwidth. The theoretical position of the
# first null is also shown.
#
# It is similar to what 01-corr-resp.py and 02-vis-plot.py do. Except
# that now the bandwidth and observing freqency are defined by the
# user.

# As of Tuesday, 30 April 2019, 10:27 AM, np.ceil(nu/Dnu) is a fudge.



#=====================================================================
#     User variables
#     Important note: Make sure that [(1/u) < (Dnu/nu)]
u             = 3           # Baseline length                             (wavelengths)
Dnu           = 8           # Bandwidth                                            (Hz)
nu            = 13          # Observing frequency                                  (Hz)
field_of_view = 180         # Total range of field of view centred on zero    (degrees)
steps         = 10000
#=====================================================================





#=====================================================================
#     Code begins here
#
nu  = float( nu)                               # Make sure frequencies are floats
Dnu = float(Dnu)

if ((1./u)/(Dnu/nu)) > 1.0:
    print "Make (1/u) <= (Dnu/nu)"
    print "   1/u = %.3f"%(1./u)
    print "Dnu/nu = %.3f"%(Dnu/nu)
    exit()

fov    = field_of_view/2.0                     # FOV centred on zero (see plot for zero)
rfov   = np.radians(fov)

xaxis  = np.linspace( fov,  -fov, steps)       # Top axis in degrees
theta  = np.linspace(rfov, -rfov, steps)       # Angular offset from perpendicular plane (radians)

l      = np.sin(theta)                         # Directional cosine ("ell") towards source, s

cosr   = np.cos(2 * np.pi * u * l)             # Interferometer cosine response, R_c
sinr   = np.sin(2 * np.pi * u * l)             # Interferometer sine   response, R_s

sinc   = np.sinc((Dnu/nu) * u * l)             # Sinc envelope [Note that in np, sinc x = sin(pi*x)/(pi*x)]

cosEnv = [i*j for i, j in zip(sinc, cosr)]     # sinc * cos
sinEnv = [i*j for i, j in zip(sinc, sinr)]     # sinc * sin

# cosEnv and sinEnv computed numerically instead:
# cosEnv = [(1/Dnu) * integrate.quad(lambda f: np.cos(2 * np.pi * u * (1/nu) * i * f), (nu-(Dnu/2)), (nu+(Dnu/2)))[0] for i in l]
# sinEnv = [(1/Dnu) * integrate.quad(lambda f: np.sin(2 * np.pi * u * (1/nu) * i * f), (nu-(Dnu/2)), (nu+(Dnu/2)))[0] for i in l]

sinTheta  = (1./u)/(Dnu/nu)                    # Compute first null...
firstNull = np.degrees(np.arcsin(sinTheta))
numFringe = np.ceil(nu/Dnu)                    #... and number of fringes to that null

print "%.1f degrees and %d fringes to the first null."%(np.degrees(np.arcsin(sinTheta)), numFringe)
#=====================================================================





#=====================================================================
#     Plotting
#
fig = plt.figure()

#==================================
#    Cosine plot params
ax1 = fig.add_subplot(121)
ax2 = ax1.twiny()                 # Create twin 'x' axis to show radians and degrees

ax1.plot(theta, cosEnv)           # Plot sinc * cos and give x-axis radians
ax2.plot(xaxis,   sinc, '--r', linewidth= 0.3)   # Plot sinc       and give x-axis degrees
ax2.axvline(firstNull, color='k', alpha= 0.2)    # Plot first null on degrees' axis

ax1.set_title( 'sinc($\\frac{'+str(int(Dnu))+' }{'+str(int(nu))+'}$ * '+str(int(u))+' * $\ell$)) * cos(2$\pi $ * '+str(int(u))+' * $\ell$)', y = 1.09)
ax1.set_ylabel('Response from correlator to square bandpass (Left:  R$_c$ , Right:  R$_s$)')
ax1.set_xlabel('Angular offset from perpendicular plane (radians)')
ax2.set_xlabel('(degrees)')

#==================================
#    Sine plot params
ax3 = fig.add_subplot(122)
ax4 = ax3.twiny()                 # Create twin 'x' axis to show radians and degrees

ax3.plot(theta, sinEnv)           # Plot sinc * sin and give x-axis radians
ax4.plot(xaxis,   sinc, '--r', linewidth= 0.3)  # Plot sinc       and give x-axis degrees
ax4.axvline(firstNull, color='k', alpha=0.3)    # Plot first null on degrees' axis

ax4.set_title( 'sinc($\\frac{'+str(int(Dnu))+' }{'+str(int(nu))+'}$ * '+str(int(u))+' * $\ell$)) * sin(2$\pi $ * '+str(int(u))+' * $\ell$)', y = 1.09)
ax3.get_yaxis().set_ticklabels([])

plt.show()
