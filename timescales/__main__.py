# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 21-01-2018 14:17:19
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import tau_stats as ts
import tau_draw as td
import input_files as f

import sys
import os
import pandas as pd

from pplib import options
from pplib import particles as pt
from pplib import parameters as p


def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

#    ct = parsed_args.particle_type

    #ts.write_to_file(f.file_path_write, symm=False) 
    #ts.write_to_file(f.file_path_write_symm) 

    data = pd.read_csv(f.file_path_write)
    data_symm = pd.read_csv(f.file_path_write_symm)
    
    td.draw_tau(data,f.data_path+"test.pdf")
    td.draw_tau_symm(data_symm,f.data_path+"model_tausg_symm.pdf")

    optimal =ts.optimize_tau_fluid(f.file_path_write_symm)

if __name__=="__main__":

    run_project(sys.argv)

