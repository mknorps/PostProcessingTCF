#s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: slice_cutter.py
# Created by: gemusia
# Creation date: 02-01-2018
# Last modified: 09-01-2018 11:33:49
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from pplib import parameters as p
from pplib import slices as s
from pplib import binary_from_fortran as bff

def cut_slice(particle_file,yplus,width=2):

    data_hrf = bff.unpack_particles_file(particle_file,p.data_dict)

    test_slices = s.SliceYplus(data_hrf,yplus,width)
    
    return test_slices


