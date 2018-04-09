#s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: slice_cutter.py
# Created by: gemusia
# Creation date: 02-01-2018
# Last modified: 09-04-2018 14:02:04
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from pplib import parameters as p
from pplib import slices as s
from pplib import tcf_parsers

def cut_slice(particle_file,yplus,width=2,ptype=0):

    data_hrf = tcf_parsers.unpack_particles_file(particle_file,p.data_dict_LES)

    test_slices = s.SliceYplus(data_hrf,yplus,width,ptype)
    
    return test_slices


