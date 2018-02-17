#s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: slice_cutter.py
# Created by: gemusia
# Creation date: 02-01-2018
# Last modified: 09-02-2018 19:56:03
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from pplib import parameters as p
from pplib import slices as s
from pplib import binary_from_fortran as bff

def cut_slice(particle_file,yplus,width=2,ptype=0):

    data_hrf = bff.unpack_particles_file(particle_file,p.data_dict_LES)

    test_slices = s.SliceYplus(data_hrf,yplus,width,ptype)
    
    return test_slices


