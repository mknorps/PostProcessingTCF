# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 09-02-2018 19:57:57
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


def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
    
    s = sc.cut_slice('/home/gemusia/wyniki/START_fields/LES/particles_3840',5,width=2,ptype=1)
    
    s.left.to_csv("~/results_for_PhD/voronoi/test_slice_St5_LES.csv")

    s.hexbin_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/hexbin_St5_LES') 
    s.scatter_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/scatter_St5_LES') 

if __name__=="__main__":

    run_project(sys.argv)

