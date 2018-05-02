import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import operator

from scipy.spatial import Voronoi, voronoi_plot_2d


def draw_histogram(pict_path, bc, theoretical, **args_experiment):
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
    args_experiment: dictionary
        distribution obtained in experiment
        keys are labels and values are data arrays

    Output
    ------
    Figure of histogram saved in pict_path    

    '''

    for arg in args_experiment.values():
        assert len(arg) == len(bc)

    fig = plt.figure(figsize = (6,4))
    ax1 = plt.subplot2grid((1,1),(0,0))

    ax1.set_xlabel("$A/\langle A\\rangle$",fontsize=15)

    ax1.plot(bc,theoretical,label="$\Gamma(a,b)$", color='black')
    for key,val in args_experiment.items():
        ax1.plot(bc,val,label=key)

    # sort legend items
    handles, labels = ax1.get_legend_handles_labels() 
    hl = sorted(zip(handles,labels),
            key=operator.itemgetter(1))
    handles2, labels2 = zip(*hl)

    leg = ax1.legend(handles2, labels2, fontsize=15)
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
    voronoi_plot_2d(vor,show_vertices=False,point_size=4)
    plt.xlim([0,2*np.pi])
    plt.ylim([0,np.pi])
 
    plt.savefig(pict_path)


