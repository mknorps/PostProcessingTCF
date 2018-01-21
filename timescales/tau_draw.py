# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: tau_draw.py
# Created by: gemusia
# Creation date: 21-01-2018
# Last modified: 21-01-2018 14:16:12
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


from pplib import parameters as p
import input_files as f

reference_data_file = f.data_path + "tau_ii.csv"
reference_data = pd.read_csv(reference_data_file)

def draw_tau_symm(data, pict_path):

        fig = plt.figure(figsize = (8,6))
        ax1 = plt.subplot2grid((1,1),(0,0)) #tme_xx

        #ax1.set_xlim([0,150])
	#ax1.set_ylim([0,60])
        ax1.tick_params(axis='both',labelsize=15)
        ax1.set_xlabel("$y^{+}$",fontsize=15)

        ax1.set_title("$\\tau^{+}$" ,fontsize=15)

        mean_tausg = (reference_data['fluid_SGSles_x']\
                     +reference_data['fluid_SGSles_y']\
                     +reference_data['fluid_SGSles_z'])/3
        Csg = {0:0.49, 1:0.49, 2:32*64*0.5}
        labels = {0:'$C_{\\tau}\\frac{\overline{\Delta}}{\sqrt{2/3k_{sg}}}$',
                  1:'$C_{\\tau}\\frac{\langle 2/3k_{sg}\\rangle}{C_{s}\Delta)^{2}|\overline{S}|^{3}}$'}

        for i in range(2):
            ax1.plot(data['y'],Csg[i]*data["tausg2_"+str(i)],label=labels[i],ls='dashed',lw=2)
        ax1.plot(150*(1+p.bins_centers_wide[:p.N_bins_wide//2]),mean_tausg,label='a priori',lw=2)


        leg = ax1.legend(fontsize=15)
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

def draw_tau(data, pict_path):

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

        for i,subplot in enumerate(ax):
            subplot.plot(p.bins_centers,data["tausg2_"+str(i)], **p.line_style_dict['fluid'])
        plt.tight_layout()
        fig.savefig(pict_path )
        plt.close(fig)

