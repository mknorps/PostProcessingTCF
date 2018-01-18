# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

import input_files as f
import compute_Ur as c
import draw

from pplib import options




def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
    
#    for key in f.prange.keys():
#        c.write_to_file(f.file_path_write+key+".csv",key)

    data = draw.Draw()
#    data.draw_ur(f.file_path_main + "ur.pdf")
#    data.draw_urnorm2(f.file_path_main + "urnorm2.pdf")
    data.draw_alpha(f.file_path_main + "alpha.pdf")

if __name__=="__main__":

    run_project(sys.argv)

