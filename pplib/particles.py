###############################################
#
#  mknorps, 11.11.2017
#
#  script for convergence check of particles 
#         simulations
#
#
###############################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pplib import parameters as p
from scipy.stats import binned_statistic

class Particles(pd.DataFrame):

    def __init__(self,data,St=('fluid',(0,p.N)),columns=[],columns_tau=[]):

        particles = {} 
        ymin = St[1][0]
        ymax = St[1][1]

        particles['x'] = data['pos'][2][ymin:ymax] % (2*np.pi)
        particles['y'] = data['pos'][0][ymin:ymax]
        particles['z'] = data['pos'][1][ymin:ymax] % (np.pi)

        for var in columns:
            particles[var] = data[var[:-2]][p.DirectionMap[var[-1]]][ymin:ymax]
            
        for var in columns_tau:
            for i in range(len(data[var])):
                particles[var+'_'+str(i)] = data[var][i][ymin:ymax]
            
        super().__init__(particles)
        self.St = St[0]


    def new_column(self,name,function,args=[]):

        self[name] =self[args].apply(lambda x: function(*x),axis=1)
        

    def bin_stat(self, columns, covariances = [], norm_factor={}):
        
        df_binned = {}
        if norm_factor == {}:
            norm_factor = {v:p.utau for v in self.columns if v!='y'}
            norm_factor['y'] = 1.0 
        for c in columns + ['y']:
            df_binned[c] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='mean')[0] )/norm_factor[c] 
            df_binned[c+"_rms"] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='std')[0] )/norm_factor[c] 
        
        for cv in covariances:
            cov = self[cv[0]]*self[cv[1]]
            df_binned[cv[0]+'_'+cv[1]] = ((binned_statistic(self['y'],cov ,bins=p.bins_y,statistic='mean')[0] )  - 
            (binned_statistic(self['y'], self[cv[0]],bins=p.bins_y,statistic='mean')[0] )*
            (binned_statistic(self['y'], self[cv[1]],bins=p.bins_y,statistic='mean')[0] ))/(norm_factor[c]**2)

        return pd.DataFrame(df_binned)

    def _pos_symm(self):
        
        nondimensional_pos = 150 * (1.0 - np.absolute(self['y']))
        return nondimensional_pos


    def map_f_init(self,f,columns):

        np_f = np.vectorize(f)

        for i in columns:
            self["f_"+i] = np_f(self[i])

