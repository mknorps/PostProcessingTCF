# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 15-01-2018 14:33:23
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from itertools import product

from pplib import parameters as p
import input_files as f


class Draw(pd.Panel):


    def __init__(self):

        data = {}

        for key in f.prange.keys(): 
            data[key] =  pd.read_csv(f.file_path_write+key+".csv")

        super().__init__(data)


    def symmetrise(self):

        symm_columns =list(set(self['St0.2'].columns) - set(f.asymm_columns)) 
        data_symm = self
        for s,c in product(f.prange.keys(),symm_columns):
            lst = data_symm[s][c]
            l = len(lst)
            data_symm[s][c] = 0.5*(lst[:(l+1)//2-1] + np.flipud(lst)[1:(l+1)//2])
        for s,c in product(f.prange.keys(),f.asymm_columns):
            lst = data_symm[s][c]
            l = len(lst)
            data_symm[s][c] = 0.5*(lst[:(l+1)//2-1] - np.flipud(lst)[1:(l+1)//2])

        for s in f.prange.keys():
            data_symm[s]['y'] = (1+data_symm[s]['y'] )*p.Retau

        
        return data_symm

    def draw_ur(self,pict_path,is_symm=True):

        fig = plt.figure(figsize = (12,6))
        ax1 = plt.subplot2grid((1,3),(0,0)) #tme_xx
        ax2 = plt.subplot2grid((1,3),(0,1)) #time_yy
        ax3 = plt.subplot2grid((1,3),(0,2)) #time_zz
        ax = [ax1,ax2,ax3]

        if is_symm:
            data = self.symmetrise()
            for figure in ax:
                figure.set_xlim([0,150])
                figure.set_ylim([-0.19,0.19])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y^{+}$",fontsize=15)
        else:
            data = self
            for figure in ax:
                figure.set_xlim([-1,1])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y$",fontsize=15)

        ax1.set_title("$u_{x}^{+}$" ,fontsize=15)
        ax2.set_title("$u_{y}^{+}$" ,fontsize=15)
        ax3.set_title("$u_{z}^{+}$" ,fontsize=15)

        for i,subplot in zip(p.DirectionList,ax):
            for particle in f.prange.keys():
                subplot.plot(data[particle]['y'],data[particle]["ur_"+i],label=particle,lw=3)

        leg = ax3.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

    def draw_alpha(self,pict_path,is_symm=True):

        beta = 0.8
        read_path = "/home/gemusia/results_for_PhD/fluid_SGS_velocity/u2sgs_stats.xls"
        ksgs_data = pd.read_excel(read_path,sheet_name="LES")
        ksgs =  2.0/3.0*(ksgs_data["u2sgs_x"][:-1]**2 +\
                ksgs_data["u2sgs_y"][:-1]**2 +\
                ksgs_data["u2sgs_z"][:-1]**2)

        data = self.symmetrise()
        fig = plt.figure(figsize = (12,6))
        ax1 = plt.subplot2grid((1,2),(0,0)) #pyyaralell
        ax2 = plt.subplot2grid((1,2),(0,1)) #tangent
        ax = [ax1,ax2]

        if is_symm:
            #data = self.symmetrise()
            for figure in ax:
                figure.set_xlim([0,150])
                figure.set_ylim([0.98,1.22])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y^{+}$",fontsize=15)
        else:
            for figure in ax:
                figure.set_xlim([-1,1])
                figure.tick_params(axis='both',labelsize=15)
                figure.set_xlabel("$y$",fontsize=15)

        ax1.set_title("$\\alpha_{\|}$" ,fontsize=15)
        ax2.set_title("$\\alpha_{\\bot}$" ,fontsize=15)

        for particle in f.prange.keys():
            urnorm2 =  (data[particle]["ur_x"]**2 +\
                   data[particle]["ur_y"]**2 +\
                   data[particle]["ur_z"]**2)
            alpha_paralell =np.sqrt(np.ones(len(urnorm2))+beta**2*np.divide(urnorm2,ksgs)) 
            alpha_orthogonal =np.sqrt(np.ones(len(urnorm2))+4*beta**2*np.divide(urnorm2,ksgs)) 
            ax1.plot(data[particle]['y'],alpha_paralell,label=particle,lw=3)
            ax2.plot(data[particle]['y'],alpha_orthogonal,label=particle,lw=3)

        leg = ax1.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

    def draw_urnorm2(self,pict_path,is_symm=True):

        data = self
        fig = plt.figure(figsize = (6,4))
        ax = plt.subplot2grid((1,1),(0,0)) 

        if is_symm:
            ax.set_xlim([0.3,150])
            #ax.set_xscale('log')
            ax.tick_params(axis='both',labelsize=15)
            ax.set_xlabel("$y^{+}$",fontsize=15)
        else:
            ax.set_xlim([-1,1])
            ax.tick_params(axis='both',labelsize=15)
            ax.set_xlabel("$y$",fontsize=15)

        ax.set_title("$k_{sg}^{+}$" ,fontsize=15)

        for particle in f.prange.keys():
            urnorm2 =  (data[particle]["ur_x"]**2 +\
                   data[particle]["ur_y"]**2 +\
                   data[particle]["ur_z"]**2)
            ax.plot(data[particle]['y'],urnorm2,label=particle,lw=3)

        leg = ax.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)
