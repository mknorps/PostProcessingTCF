#
# File name: slice_concentration.py
# Created by: gemusia
# Creation date: 02-01-2018
# Last modified: 26-01-2018 16:14:46
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pplib import parameters as p
from pplib import slices as s


class SliceConc(pd.DataFrame):


    def conc_histogram(self,binedges):

        xdata = self['x']
        ydata = self['z']
        H,xedges,yedges = np.histogram2d(xdata, ydata, bins=binedges,normed=True)
       
        bins2d = H.flatten()
        h,bins =np.histogram(bins2d,normed=True)

        return h
