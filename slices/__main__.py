# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: __main__.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 30-04-2018 11:39:52
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

dir_path ='/home/mknorps/Projects/ForPhD/PostProcessingTCF/' 
# append src module to inport paths
sys.path.append(dir_path)

from pplib import options
from pplib import parameters as p
from pplib import slices as s
from pplib import slice_cutter as sc
from pplib import halo as hl

def cut_with_halo(in_dir, out_dir,
        input_file, output_file_core, ptype, yplus=5, offset = 0.3):
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

    s = sc.cut_slice(in_dir+input_file, yplus, width=3, ptype=ptype)

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
   

    in_dir = "/home/mknorps/Projects/ForPhD/SPECTRAL_from2011/FRACTAL/"
    out_dir = "/home/mknorps/Projects/ForPhD/SPECTRAL_from2011/FRACTAL/slices/"
    f_min = 880
    f_max = 900
    for ptype in range(4):
        for i in range(f_min, f_max):
            input_file = 'particles_0{}'.format(i)
            output_file_core = "slice_FRACTAL_center_{}_{}".format(p.StList2[ptype],i)
            cut_with_halo(in_dir, out_dir, input_file, output_file_core, ptype, yplus=145)


if __name__=="__main__":

    run_project(sys.argv)

