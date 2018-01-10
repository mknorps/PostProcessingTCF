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
import u2sgs_draw as d

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

    s.write_to_file(f.file_path_write)

    data = d.DrawU2sgs()
    data.draw_u2sgs(f.file_path_main + "u2sgs.pdf")
    data.draw_ksgs(f.file_path_main + "ksgs.pdf")
    data.draw_cov_xy(f.file_path_main + "cov_xy.pdf")

if __name__=="__main__":

    run_project(sys.argv)

