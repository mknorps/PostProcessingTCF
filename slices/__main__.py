# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 21-02-2018 23:25:20
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

from pplib import options
from pplib import parameters as p
from pplib import slices as s
from pplib import slice_cutter as sc

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

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
   

    for ptype in range(4):
        for i in range(4860,4881):
            s = sc.cut_slice('/home/gemusia/results_for_PhD/voronoi/particle_fields/LES_nomodel/particles_{}'.format(i),5,width=2,ptype=ptype)

            left_slice_halo = points_with_halo(s.left,'x','z')
            right_slice_halo = points_with_halo(s.right,'x','z')
            left_slice_halo.to_csv("/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_{}_{}_left.csv".format(p.StList2[ptype],i))
            right_slice_halo.to_csv("/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_{}_{}_right.csv".format(p.StList2[ptype],i))

    #s.hexbin_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/hexbin_St5_LES') 
    #s.scatter_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/scatter_St5_LES') 

if __name__=="__main__":

    run_project(sys.argv)

