# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
#
# Computations of mean dissipation of kinetic energy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

import input_files as f
import diss_draw as d
import diss_stats as s

from pplib import options




def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
    

    s.write_to_file(f.file_path_write)
    s.symmetrise(f.file_path_write,f.file_path_symm )

    d.draw_diss_tot(f.file_path_symm, f.file_path_main + "diss.pdf")
    d.draw_diss_model(f.file_path_symm, f.file_path_main + "diss_model.pdf")

if __name__=="__main__":

    run_project(sys.argv)

