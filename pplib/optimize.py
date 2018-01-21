# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: optimize.py
# Created by: gemusia
# Creation date: 22-12-2017
# Last modified: 21-01-2018 13:47:42
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import pandas as pd
import scipy.optimize as opt
from inspect import signature

def fit_data_series(y,f):

    def l2norm(f,y):
        def l2norm_curr(a):
            n = np.linalg.norm(f-a*y,ord=2)
            return n
        return l2norm_curr
    optimal =  opt.minimize_scalar(l2norm(f,y)) 

    return optimal

class Optimize(pd.DataFrame):

    def __init__(self,tausg):

        super(Optimize,self).__init__(tausg)


    def fit(self, f = lambda x,a : a , xcol='y', ycols=['tausg1']):

        rows_count = len(self)
        sig = signature(f)

        x0 = np.zeros(len(sig.parameters)-1) #initial guess
        sigma = np.ones(rows_count) # in chisquare statistics

        xdata = self[xcol]

        if type(ycols) == 'string':
            ycols = list[ycols]

        param = {}
        cov_matr = {}
        for col in ycols:
            ydata = self[col]
            param[col],cov_matr[col] = opt.curve_fit(f,xdata,ydata,x0,sigma) 
    
        return [param,cov_matr]

    def fit_several(self,f = lambda x,a : a,xcol='y', ycols=['tausg2_x','tausg2_y','tausg2_z']):

        ycols_count = len(ycols)
        self_xcols = [self['y'] for _ in range(ycols_count)]
        xcolspd = pd.concat(self_cols) 
        self_ycols = [self[c] for c in ycols]
        ycolspd = pd.concat(self_ycols)

        return self.fit(f,xcolspd,ycolspd)



    def fit_data(self, fdata, xcol='y'):

        ycols =[x for x in self.columns if x.startswith("tausg")]
        xdata = self[xcol]
        xdataf = fdata[xcol]

        if not np.allclose(xdata,xdataf):
            print ("uncomparable data", xdata, xdataf)
            return None

        param = {}
        for col in ycols:
            y = self[col]
            f = fdata[col]
            param[col] = opt.minimize_scalar(l2norm(f,y)) 
  
        # one parameter for all directions of tausg2
        ycols_tausg2 = [x for x in ycols if x.startswith("tausg2")]
        if ycols_tausg2:
            y=pd.concat([self[a] for a in ycols_tausg2])
            f=pd.concat([fdata[a] for a in ycols_tausg2])
            param['tausg2'] =fit_data_series(y,f)

        return param

