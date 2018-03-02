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

from pplib import halo 


def draw_histogram(pict_path, bc, *args_experiment, theoretical = None):
    '''
    Draw histogram and save it as pict_path

    Parameters
    ----------
    pict_path : str
        file name to save plot
    bc : list of floats
        bin centers
    theoretical: array(float), optional 
        theoretical distribution
    args_experiment: list
        distribution obtained in experiment
        single element is a dictionary:
        {'data':array(float), 'label':str}

    Output
    ------
    Figure of histogram saved in pict_path    

    '''

    for arg in args_experiment:
        assert len(arg['data']) == len(bc)

    fig = plt.figure(figsize = (6,4))
    ax1 = plt.subplot2grid((1,1),(0,0))

    ax1.set_xlabel("$A/\langle A\\rangle$",fontsize=15)

    ax1.plot(bc,theoretical,label="$\Gamma(a,b)$", color='black')
    for arg in args_experiment:
        ax1.plot(bc,arg['data'],label=arg['label'])

    leg = ax1.legend(fontsize=15)
    plt.tight_layout()
    fig.savefig(pict_path)
    plt.close(fig)


def draw_voronoi_from_slice(input_file, pict_path, usecols=["x","z"]):
    '''
    Draw voronoi polygons and save it as pict_path

    Parameters
    ----------
    pict_path : str
        file name to save plot
    points : array
        
    Output
    ------
    Graphical interpretation of Voronoitessalation
    saved in pict_path    

    '''
    points = pd.read_csv(input_file, usecols=usecols)
    vor = Voronoi(points)
    voronoi_plot_2d(vor,show_vertices=False,point_size=1)
    
    plt.savefig(pict_path)


def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    slice_file = "/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_St25_4860_left.csv"
    pict_path = "/home/gemusia/results_for_PhD/voronoi/slices/LES/voronoi_snapshot_LES_St25.eps"
    draw_voronoi_from_slice(slice_file, pict_path)

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

