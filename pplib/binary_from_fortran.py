###############################################
#
#  mknorps, 11.11.2017
#
#  script for convergence check of particles 
#         simulations
#
#
###############################################


import struct
import numpy as np
import os


fortran_write_nbytes = 4
type_prefix = {"integer":"i", "real":"d"}

def get_no_of_elements(datainfo_dict):

    if "shape" in datainfo_dict:
        n = np.prod(np.array(datainfo_dict["shape"]))
    else:
        n = 1
    return n

def get_no_of_bytes(datainfo_dict,nelements):

    nbytes = datainfo_dict["size"]

    return nbytes*nelements

def unpack_particles_file(f,data_dict):
   
    f_size = os.path.getsize(f)
    with open(f, mode='rb') as ff:
        data_bin = ff.read()

    read_data = {}
    bmin = 0
    bmax = 0

    for key,val in data_dict.items():
   
        nelements = get_no_of_elements(val)
        prefix = type_prefix[val["type"]]

        bmin = bmin + fortran_write_nbytes
        bmax = bmin + get_no_of_bytes(val,nelements)

        data = struct.unpack(prefix * (nelements),data_bin[bmin:bmax] )

        if (nelements>1) :
            data_reshaped = np.array(data).reshape(tuple(val["shape"]))
            data = data_reshaped

        bmax = bmax + fortran_write_nbytes
        bmin = bmax

        read_data[key] = data

    assert (bmax == f_size)
    return read_data 


    
