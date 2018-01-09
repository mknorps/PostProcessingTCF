# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 09-01-2018 18:55:36
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
from pplib import parameters as p


def read_from_excel():

    data = pd.read_excel(f.file_path_write)
    return data

def draw_u2sgs(pict_path,data):
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

    ax1.set_title("$u_{x}^{+}$" ,fontsize=15)
    ax2.set_title("$u_{y}^{+}$" ,fontsize=15)
    ax3.set_title("$u_{z}^{+}$" ,fontsize=15)

    for i,subplot in zip(p.DirectionList,ax):
        for simulation in f.types:
            subplot.plot(data[simulation]['y'],data[simulation]["usgs_"+i+"_rms")

    leg = ax3.legend(fontsize=15)
    plt.tight_layout()
    fig.savefig(pict_path )
    plt.close(fig)
