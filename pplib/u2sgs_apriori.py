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

class U2sgs(pd.DataFrame):

    def __init__(self,data):

        tausg = {} 
        tausg['x'] = data['pos'][2] % (2*np.pi)
        tausg['y'] = data['pos'][0]
        tausg['z'] = data['pos'][1] % (np.pi)

        tausg['usgs_x'] = data['upar'][2] - data['uparf'][2] 
        tausg['usgs_y'] = data['upar'][0] - data['uparf'][0] 
        tausg['usgs_z'] = data['upar'][1] - data['uparf'][1] 
        tausg['upar_x'] = data['upar'][2]
        tausg['upar_y'] = data['upar'][0]
        tausg['upar_z'] = data['upar'][1]
        tausg['uparf_x'] = data['uparf'][2]
        tausg['uparf_y'] = data['uparf'][0]
        tausg['uparf_z'] = data['uparf'][1]
        tausg['cov_xy'] = (data['upar'][2] - data['uparf'][2])*(data['upar'][0] - data['uparf'][0]) 

        super().__init__(tausg)

    def bin_stat(self, columns, covariances = []):
        
        df_binned = {}
        norm_factor = {v:p.utau for v in self.columns if v!='y'}
        norm_factor['y'] = 1.0 
        for c in columns + ['y']:
            df_binned[c] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='mean')[0] )/norm_factor[c] 
            df_binned[c+"_rms"] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='std')[0] )/norm_factor[c] 
        
        for cv in covariances:
            cov = self[cv[0]]*self[cv[1]]
            df_binned[cv[0]+'_'+cv[1]] = ((binned_statistic(self['y'],cov ,bins=p.bins_y,statistic='mean')[0] )  - 
            (binned_statistic(self['y'], self[cv[0]],bins=p.bins_y,statistic='mean')[0] )*
            (binned_statistic(self['y'], self[cv[0]],bins=p.bins_y,statistic='mean')[0] ))/(norm_factor[c]**2)

        return pd.DataFrame(df_binned)

    def _pos_symm(self):
        
        nondimensional_pos = 150 * (1.0 - np.absolute(self['y']))
        return nondimensional_pos


    def map_f_init(self,f,columns):

        np_f = np.vectorize(f)

        for i in columns:
            self["f_"+i] = np_f(self[i])

