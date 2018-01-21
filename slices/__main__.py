# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 21-01-2018 10:44:57
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
    
    s = sc.cut_slice('/home/gemusia/wyniki/time_scales_modelled/from_tryton/case_45/particles_2905',5)

    s.hexbin_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/hexbin_test') 
    s.scatter_plot('/home/gemusia/wyniki/time_scales_modelled/pictures/scatter_test') 

if __name__=="__main__":

    run_project(sys.argv)

