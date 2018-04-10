# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 10-04-2018 12:50:41
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

def cut_with_halo(in_dir, out_dir,
        input_file, output_file_core, ptype, offset = 0.3):
    '''
    cut slice from particle positions for  y^{+}=5
    writes it to a csv file

    Parameters
    ----------
    in_dir - directory were particle files from 
            Fortran computations are located
    input_file - particle file in binary format
    output_file_core - core of the output file name 
    out_dir - directory for the result (slices)
    offset - size of halo around the slice

    Output
    ------
    particles_slice - dataframe with positions of particles

    Result
    ------
    Slices cut and written to CSV files
    '''

    s = sc.cut_slice(in_dir+input_file, 5, width=2, ptype=ptype)

    left_slice_halo = hl.points_with_halo(s.left,'x','z',offset)
    right_slice_halo = hl.points_with_halo(s.right,'x','z',offset)
    left_slice_halo.to_csv(out_dir + output_file_core + "_left.csv")
    right_slice_halo.to_csv(out_dir + output_file_core + "_right.csv")

    return left_slice_halo



def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
   

    in_dir = "/home/gemusia/results_for_PhD/voronoi/particle_fields/DNS/"
    out_dir = "/home/gemusia/results_for_PhD/voronoi/slices/DNS/"
    f_min = 2620
    f_max = 2640
    for ptype in range(4):
        for i in range(f_min, f_max):
            input_file = 'particles_{}'.format(i)
            output_file_core = "slice_DNS_{}_{}".format(p.StList2[ptype],i)
            cut_with_halo(in_dir, out_dir, input_file, output_file_core, ptype)


if __name__=="__main__":

    run_project(sys.argv)

