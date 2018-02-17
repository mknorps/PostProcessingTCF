# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

from scipy.spatial import Voronoi, voronoi_plot_2d

from pplib import options


def point_halo(points):

    xmin = min(points['x'])
    xmax = max(points['x'])
    ymin = min(points['y'])
    ymax = max(points['y'])

    halo = points['x'].apply()


def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    points = pd.read_csv("~/results_for_PhD/voronoi/test_slice_St5_LES.csv",usecols=["x","z"])
    vor = Voronoi(points)
    print (dir(vor))
    print (vor.vertices)
    
    voronoi_plot_2d(vor,show_vertices=False,point_size=1)
    plt.show()



if __name__=="__main__":

    run_project(sys.argv)

