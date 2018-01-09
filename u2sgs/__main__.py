# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs.py
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import sys
import os
import pandas as pd

from pplib import options
from pplib import parameters as p
from pplib import u2sgs_apriori as ua
from pplib import binned_u2sgs as bu
from pplib import binary_from_fortran as bff


def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    y = parsed_args.slice_yplus

    if y :
        print('Hello! ', y)
    
    particle_file = "/home/gemusia/wyniki/apriori/heavy_particles_2580"
    data_hrf = bff.unpack_particles_file(particle_file,p.data_dict3)

    d = ua.U2sgs(data_hrf)
    df = bu.BinnedTau(d.df)
    binned = df.bin_stat(['usgs_x','usgs_y','usgs_z',
                          'upar_x','upar_y','upar_z',
                          'uparf_x','uparf_y','uparf_z' ])

    print(binned)

if __name__=="__main__":

    run_project(sys.argv)

