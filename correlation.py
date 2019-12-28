#! /usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

# Written by Vasaant S/O Krishnan on Tuesday, 21 August 2018

# correlation.py correlates two cosine waves which are simulated to be
# the response of a 2-element interferometer. However, I need further
# understanding still.
# Search for ***

#=====================================================================
#     User variables
#
u             = 3           # Baseline length                             (wavelengths)
nu            = 5           # Centre freq.                                         (Hz)
signal        = 6000        # Signal duration                                     (sec)
field_of_view = 180         # Total range of field of view centred on zero    (degrees)
steps         = 2000
#=====================================================================





#=====================================================================
#     Code begins here
#
fov   = field_of_view/2.0                  # FOV centred on zero (see plot for zero)
rfov  = np.radians(fov)
theta = np.linspace(rfov, -rfov, steps)    # Angular offset from perpendicular plane (radians)

l     = np.sin(theta)                      # Directional cosine ("ell") towards source, s

w     = 2*np.pi*nu                         # Angular freq.
c     = 1                                  # Speed of light
tau_G = u*l*1/c

t   = np.linspace(signal, -signal, steps)
wn  = np.random.normal(0, 1, t.shape)      # White noise

v1  = wn + np.cos( w* t)
v2  = wn + np.cos([w*(i-j) for i, j in zip(t, tau_G)])

vv  = (1./signal)*np.correlate(v1, v2, mode= 'same')

plt.subplot(211)
plt.plot(t, v1, c='b', alpha=0.6, label='v1')
v2 = [10+i for i in v2]
plt.plot(t, v2, c='g', alpha=0.6, label='v2')
plt.xlim([-signal/3,signal/3])
plt.legend()

plt.subplot(212)
plt.plot(  t, vv, color='k', label='<vv>')
plt.xcorr(v1, v2, color='r')               # Built-in cross correlation plotter
plt.xlim([-signal/3,signal/3])
plt.legend()

plt.show()
#=====================================================================




# nFreqs        = 10          # No. of freqs to constitute a "multi"chromatic wave

# freqs = np.linspace(nu+nu/2, nu-nu/2, nFreqs)  # Create frequencies for a "multi"chromatic function

# cos = lambda x: np.cos(x* t)
# v1  = np.zeros((len(t), len(freqs)))      # shape (steps, nFreqs)
# v2  = np.zeros((len(t), len(freqs)))

# ts  = np.asarray(len(freqs)*[t])          # shape (nFreqs, steps)


# a = np.outer(ts, freqs)
# print a
# print np.shape(a)

# # ts  = np.reshape(ts, (len(t), len(freqs)))

# for i in freqs:
#     v1 = np.cos(2*np.pi*i * t)


# w = 2*np.pi*nu                       # Omega
