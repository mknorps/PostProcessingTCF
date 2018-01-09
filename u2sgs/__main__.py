# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

import input_files as f

from pplib import options
from pplib import parameters as p
from pplib import u2sgs_apriori as ua
from pplib import binary_from_fortran as bff



def compute_bin_stats():

    for particle_file in f.files_def:

        data_hrf = bff.unpack_particles_file(particle_file,p.data_dict_apriori)
        d = ua.U2sgs(data_hrf)
        df = bu.BinnedTau(d.df)
        binned = df.bin_stat(['usgs_x','usgs_y','usgs_z',
                              'upar_x','upar_y','upar_z',
                              'uparf_x','uparf_y','uparf_z' ])

    

def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
    
    particle_file = "/home/gemusia/wyniki/apriori/heavy_particles_2580"
    data_hrf = bff.unpack_particles_file(particle_file,p.data_dict_apriori)

    d = ua.U2sgs(data_hrf)

    print(type(d))
    binned = d.bin_stat(['usgs_x','usgs_y','usgs_z',
                          'upar_x','upar_y','upar_z',
                          'uparf_x','uparf_y','uparf_z' ])

    print(binned)

if __name__=="__main__":

    run_project(sys.argv)

