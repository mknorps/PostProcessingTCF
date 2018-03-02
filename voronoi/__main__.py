# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Voronoi, voronoi_plot_2d

from pplib import options
from pplib import halo 


def draw_histogram(pict_path,x,theoretical,*args_experiment):

    fig = plt.figure(figsize = (6,4))
    ax1 = plt.subplot2grid((1,1),(0,0)) #tme_xx

    ax1.set_xlabel("$A/\langle A\\rangle$",fontsize=15)

    ax1.plot(x,theoretical,label="$\Gamma(a,b)$", color='black')
    for arg in args_experiment:
        ax1.plot(x,arg['data'],label=arg['label'])

    leg = ax1.legend(fontsize=15)
    plt.tight_layout()#
    fig.savefig(pict_path )
    plt.close(fig)

def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    points = pd.read_csv("/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_St25_4860_left.csv",usecols=["x","z"])
    #vor = Voronoi(points)
    #plt.ion()
    #voronoi_plot_2d(vor,show_vertices=False,point_size=1)
    #plt.hold(True)

    df = halo.points_with_halo(points,'x','z',0.1)
 
    print(df.head())
    print(df.describe())


    #vor = Voronoi(df)
    #voronoi_plot_2d(vor,show_vertices=False,point_size=3)
    #plt.show()

    #plt.hold(False)

    data_St1 = np.loadtxt("/home/gemusia/kody/voronoi_IMP/hist_FRACTAL_St1.res",skiprows=5)
    data_St5 = np.loadtxt("/home/gemusia/kody/voronoi_IMP/hist_FRACTAL_St5.res",skiprows=5)
    data_St25 = np.loadtxt("/home/gemusia/kody/voronoi_IMP/hist_FRACTAL_St25.res",skiprows=5)

    results_St1 = {'data':data_St1[:,2], 'label':"St1"}
    results_St5 = {'data':data_St5[:,2], 'label':"St5"}
    results_St25 = {'data':data_St25[:,2], 'label':"St25"}
    draw_histogram("Voronoi_his_FRACTAL.eps",data_St1[:,0],data_St1[:,1],
            results_St1, results_St5, results_St25)



if __name__=="__main__":

    run_project(sys.argv)

