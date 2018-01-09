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
from scipy.stats import binned_statistic


from pplib import parameters as p


class BinnedTau(pd.DataFrame):


    def _pos_symm(self):
        
        nondimensional_pos = 150 * (1.0 - np.absolute(self['y']))
        return nondimensional_pos


    def map_f_init(self,f,columns):

        np_f = np.vectorize(f)

        for i in columns:
            self["f_"+i] = np_f(self[i])

    def bin_stat(self, columns):
        
        df_binned = {}
        norm_factor = {v:p.utau for v in self.columns if v!='y'}
        norm_factor['y'] = 1.0 
        for c in columns:
            df_binned[c] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='mean')[0] )/norm_factor[c] 
            df_binned[c+"_rms"] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='std')[0] )/norm_factor[c] 
        
        return pd.DataFrame(df_binned)
