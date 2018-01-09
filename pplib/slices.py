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


class SliceYplus:

    def __init__(self,data,yplus,width):

        tausg = {} 
        tausg['x'] = data['pos'][2] % (2*np.pi)
        tausg['y'] = data['pos'][0]
        tausg['z'] = data['pos'][1] % (np.pi)

        self._init_slice(tausg, yplus,width)


    def _init_slice(self,tausg,yplus,width):

        df = pd.DataFrame(tausg)

        df['yplus'] = df['y'].apply(p.y_plus)  
        self.left = df.loc[df['yplus'].between(yplus-width,yplus+width)]
        self.right = df.loc[df['yplus'].between(2*p.Retau-yplus-width,2*p.Retau-yplus+width)]

    def scatter_plot(self,pict_path):
        
        left_df = self.left
        right_df = self.right
        left_df.plot(kind='scatter',x='x',y='z',s=1)
        plt.savefig(pict_path+"_left.pdf" )
        right_df.plot(kind='scatter',x='x',y='z',s=1)
        plt.savefig(pict_path+"_right.pdf" )

    def hexbin_plot(self,pict_path):
        
        left_df = self.left
        right_df = self.right
        left_df.plot(kind='hexbin',x='x',y='z',mincnt=2)
        plt.savefig(pict_path+"_left.pdf" )
        right_df.plot(kind='hexbin',x='x',y='z')
        plt.savefig(pict_path+"_right.pdf" )


    def draw_tau(self,st_list,pict_path):
        binstat = self.bin_stat(st_list)
        Csg =0.5 
        fig = plt.figure(figsize = (12,6))
        ax1 = plt.subplot2grid((1,3),(0,0)) #tme_xx
        ax2 = plt.subplot2grid((1,3),(0,1)) #time_yy
        ax3 = plt.subplot2grid((1,3),(0,2)) #time_zz
        ax = [ax1,ax2,ax3]

        for figure in ax:
            figure.set_xlim([-1,1])
            #figure.set_ylim([0,60])
            figure.tick_params(axis='both',labelsize=15)
            figure.set_xlabel("$y$",fontsize=15)

        ax1.set_title("$\\tau_{x}^{+}$" ,fontsize=15)
        ax2.set_title("$\\tau_{y}^{+}$" ,fontsize=15)
        ax3.set_title("$\\tau_{z}^{+}$" ,fontsize=15)

        for i,subplot in zip(p.DirectionList,ax):
            for x in st_list:
                subplot.plot(p.bins_centers,binstat[x]["tausg2_"+i], **p.line_style_dict[x])

        leg = ax3.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)
