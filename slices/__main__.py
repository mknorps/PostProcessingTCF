# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 28-02-2018 21:57:21
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
from pplib import halo as hl


def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
   

    for ptype in range(4):
        for i in range(4860,4881):
            s = sc.cut_slice('/home/gemusia/results_for_PhD/voronoi/particle_fields/LES_nomodel/particles_{}'.format(i),5,width=2,ptype=ptype)

            left_slice_halo = hl.points_with_halo(s.left,'x','z',0.3)
            right_slice_halo = hl.points_with_halo(s.right,'x','z',0.3)
            left_slice_halo.to_csv("/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_{}_{}_left.csv".format(p.StList2[ptype],i))
            right_slice_halo.to_csv("/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_{}_{}_right.csv".format(p.StList2[ptype],i))

    #s.hexbin_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/hexbin_St5_LES') 
    #s.scatter_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/scatter_St5_LES') 

if __name__=="__main__":

    run_project(sys.argv)

