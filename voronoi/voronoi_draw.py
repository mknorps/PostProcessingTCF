import pandas as pd
import matplotlib.pyplot as plt

from scipy.spatial import Voronoi, voronoi_plot_2d


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


