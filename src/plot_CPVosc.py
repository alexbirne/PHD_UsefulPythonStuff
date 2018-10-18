#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to plot time dependent CP oscillation and sensitiv regions in Bd2Dpi schematically."""

import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import os

plot_path = "/net/nfshome/home/abirnkraut/Bd2Dpi_CPV/output/asymmetry/sensitivity/"

deltaM = 0.505
Sf = -0.0307618
Sfbar = -0.0285073
Cf = 0.9994
Cfbar = -0.9994

time = np.linspace(0.4, 12.0, 100)
sin_function = np.sin(deltaM * time)
cos_function = np.cos(deltaM * time)
horizon = np.zeros((100))

#  plotting finalstate f
plt.rc('text', usetex=True)
plt.figure(figsize=(10, 6))
plt.plot(time, Sf * sin_function, ls='-.', color='#7570b3', linewidth = 2.0, label='$S_{f}\cdot\sin(\Delta mt)$')
plt.plot(time, Cf * cos_function, ls='--', color='#d95f02', linewidth = 2.0, label='$C_{f}\cdot\cos(\Delta mt)$')
plt.plot(time, Sf * sin_function + Cf * cos_function, color = 'black', linewidth = 2.0, label='$C_{f}\cdot\cos(\Delta mt) - S_{f}\cdot\sin(\Delta mt)$')
plt.plot(time, horizon, color = 'black')
plt.fill_between(time, -1, 1, where=abs(cos_function) < 0.25, facecolor = 'none',
                 edgecolor='#1b9e77', hatch = '////', linewidth = 0.0, zorder = 0,
                 label = 'sensitive region')

plt.ylabel('$C\!P$ asymmetry', fontsize=25)
plt.xlabel('$t_{B^{\kern 0.6pt 0}} \mathrm{(ps)}$', fontsize=30)
plt.legend(loc='upper center', fontsize=15)
plt.tight_layout()
axes = plt.gca()
axes.set_xlim([0.4, 12.0])
axes.set_ylim([-1.0, 1.0])

majorLocator_x = ticker.MultipleLocator(1)
majorLocator_y = ticker.MultipleLocator(0.2)
minorLocator_y = ticker.MultipleLocator(0.05)
majorFormatter = ticker.ScalarFormatter()
axes.xaxis.set_major_locator(majorLocator_x)
axes.xaxis.set_major_formatter(majorFormatter)
for tick in axes.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

axes.yaxis.set_major_locator(majorLocator_y)
axes.yaxis.set_minor_locator(minorLocator_y)
axes.yaxis.set_major_formatter(majorFormatter)
for tick in axes.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

# saving the plot into pdf and tex
if not os.path.exists(plot_path):
    os.makedirs(plot_path)
# plt.show()
plt.savefig(plot_path + 'oscillation_f.pdf')
from matplotlib2tikz import save as tikz_save
tikz_save(plot_path + 'oscillation_f.tex')

# plotting finalstate_fbar
plt.rc('text', usetex=True)
plt.figure(figsize=(10, 6))
plt.plot(time, Sfbar * sin_function, ls='-.', color='#7570b3', linewidth = 2.0, label='$S_{\overline{\kern -1.5pt f\kern 0.2pt}}\cdot\sin(\Delta mt)$')
plt.plot(time, Cfbar * cos_function, ls='--', color='#d95f02', linewidth = 2.0, label='$C_{\overline{\kern -1.5pt f\kern 0.2pt}}\cdot\cos(\Delta mt)$')
plt.plot(time,
         Sfbar * sin_function + Cfbar * cos_function,
         color = 'black', linewidth = 2.0,
         label='$C_{\overline{\kern -1.5pt f\kern 0.2pt}}\cdot\cos(\Delta mt) - S_{\overline{\kern -1.5pt f\kern 0.2pt}}\cdot\sin(\Delta mt)$')
plt.plot(time, horizon, color = 'black')
plt.fill_between(time, -1, 1, where=abs(cos_function) < 0.25, facecolor = 'none',
                 edgecolor='#1b9e77', hatch = '////', linewidth = 0.0, zorder = 0,
                 label = 'sensitive region')

plt.ylabel('$C\!P$ asymmetry', fontsize=25)
plt.xlabel('$t_{B^{\kern 0.6pt 0}} \mathrm{(ps)}$', fontsize=30)
plt.legend(loc='lower center', fontsize=15)
plt.tight_layout()
axes = plt.gca()
axes.set_xlim([0.4, 12.0])
axes.set_ylim([-1.0, 1.0])

majorLocator_x = ticker.MultipleLocator(1)
majorLocator_y = ticker.MultipleLocator(0.2)
minorLocator_y = ticker.MultipleLocator(0.05)
majorFormatter = ticker.ScalarFormatter()
axes.xaxis.set_major_locator(majorLocator_x)
axes.xaxis.set_major_formatter(majorFormatter)
for tick in axes.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

axes.yaxis.set_major_locator(majorLocator_y)
axes.yaxis.set_minor_locator(minorLocator_y)
axes.yaxis.set_major_formatter(majorFormatter)
for tick in axes.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

# saving the plot into pdf and tex
# plt.show()
plt.savefig(plot_path + 'oscillation_fbar.pdf')
tikz_save(plot_path + 'oscillation_fbar.tex')
