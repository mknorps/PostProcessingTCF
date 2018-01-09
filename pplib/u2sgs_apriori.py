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

        super().__init__(tausg)

    def bin_stat(self, columns, pfields=()):
        
        df_binned = {}
        norm_factor = {v:p.utau for v in self.columns if v!='y'}
        norm_factor['y'] = 1.0 
        for c in columns:
            df_binned[c] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='mean')[0] )/norm_factor[c] 
            df_binned[c+"_rms"] = (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='std')[0] )/norm_factor[c] 

            for field in pfields:
                df_binned[c] = df_binned[c] + (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='mean')[0] )/norm_factor[c] 
                df_binned[c+"_rms"] = df_binned[c] + (binned_statistic(self['y'], self[c],bins=p.bins_y,statistic='std')[0] )/norm_factor[c] 


            df_binned[c] = df_binned[c]/(len(pfields)+1)
            df_binned[c+"_rms"] = df_binned[c+"_rms"]/(len(pfields)+1)
        
        return pd.DataFrame(df_binned)

    def _pos_symm(self):
        
        nondimensional_pos = 150 * (1.0 - np.absolute(self['y']))
        return nondimensional_pos


    def map_f_init(self,f,columns):

        np_f = np.vectorize(f)

        for i in columns:
            self["f_"+i] = np_f(self[i])

    def draw_tau(self, pict_path):
        fig = plt.figure(figsize = (12,6))
        ax1 = plt.subplot2grid((1,3),(0,0)) #tme_xx
        ax2 = plt.subplot2grid((1,3),(0,1)) #time_yy
        ax3 = plt.subplot2grid((1,3),(0,2)) #time_zz
        ax = [ax1,ax2,ax3]

        for figure in ax:
            figure.set_xlim([-1,1])
            figure.tick_params(axis='both',labelsize=15)
            figure.set_xlabel("$y$",fontsize=15)

        ax1.set_title("$u_{x}^{+}$" ,fontsize=15)
        ax2.set_title("$u_{y}^{+}$" ,fontsize=15)
        ax3.set_title("$u_{z}^{+}$" ,fontsize=15)

        #for i,subplot in zip(p.DirectionList,ax):
            #subplot.plot(,binstat[x]["tausg2_"+i], **p.line_style_dict[x])

        leg = ax3.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)
