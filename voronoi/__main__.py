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


def points_with_halo(points,col1,col2):

    xmin = min(points[col1])
    xmax = max(points[col1])
    ymin = min(points[col2])
    ymax = max(points[col2])

    #vertical halo
    halo_offset = (xmax-xmin)/2
    top_half = points[points[col1]>halo_offset]
    bottom_half = points[points[col1]<halo_offset]

    top_half.loc[:,col1] = top_half[col1] - (xmax-xmin)
    bottom_half.loc[:,col1] = bottom_half[col1] +(xmax-xmin)

    vertical_halo = pd.concat([points,top_half,bottom_half],ignore_index=True)

    #horisontal halo
    halo_offset = (ymax-ymin)/2
    right_half = vertical_halo[vertical_halo[col2]>halo_offset]
    left_half = vertical_halo[vertical_halo[col2]<halo_offset]

    right_half.loc[:,col2] = right_half[col2] - (ymax-ymin)
    bottom_half.loc[:,col2] = bottom_half[col2] +(ymax-ymin)

    df = pd.concat([vertical_halo,right_half,left_half],ignore_index=True)

    return df

def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    points = pd.read_csv("~/results_for_PhD/voronoi/test_slice_St5_LES.csv",usecols=["x","z"])
    #vor = Voronoi(points)
    #plt.ion()
    #voronoi_plot_2d(vor,show_vertices=False,point_size=1)
    #plt.hold(True)

    df = points_with_halo(points,'x','z')
 
    print(df.head())
    print(df.describe())


    vor = Voronoi(df)
    voronoi_plot_2d(vor,show_vertices=False,point_size=1)
    plt.show()
    #plt.hold(False)


if __name__=="__main__":

    run_project(sys.argv)

