#
# File name: slice_concentration.py
# Created by: gemusia
# Creation date: 02-01-2018
# Last modified: 09-01-2018 11:33:48
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
       
        print(sum(H))
        bins2d = H.flatten()
        h,bins =np.histogram(bins2d,normed=True)

        print(h)
        return h
