# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

import input_files as f
import u2sgs_stats as s

from pplib import options
from pplib import parameters as p
from pplib import u2sgs_apriori as ua
from pplib import binary_from_fortran as bff




def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
    
    particle_file = "/home/gemusia/wyniki/apriori/heavy_particles_2580"

    s.compute_bin_stats_def()
    stats_LES = s.compute_bin_stat_LES()
    print(stats_LES.head())

if __name__=="__main__":

    run_project(sys.argv)

