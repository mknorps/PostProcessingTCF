
import re
import struct
import numpy as np
import pandas as pd
from collections import OrderedDict
from os.path import exists, getsize




def unpack_particles_file(input_file : str, 
                          data_dict : OrderedDict):
    '''
    parse raw particle files 
    generated by Fortan spectral channel flow code
    as a binary output

    Input
    -----
    input_file - path to the input file
    data_dict  - OrderedDict with variable name as a key
                 and a value of a dictionary with keys:
                 "size" - size of a variable type in bytes
                 "shape" (optional) - shape of the variable array
                 "type": "i" - integer and "d" - real

    Output
    ------
    read_data - dictionary with the column names as keys 
                and values in a numercal format
    '''
    fortran_write_nbytes = 4
    f_size = getsize(input_file)
    with open(input_file, mode='rb') as ff:
        data_bin = ff.read()

    read_data = {}
    bmin = 0
    bmax = 0

    def get_no_of_elements(datainfo_dict):

        if "shape" in datainfo_dict:
            n = np.prod(np.array(datainfo_dict["shape"]))
        else:
            n = 1
        return n

    def get_no_of_bytes(datainfo_dict,nelements):

        nbytes = datainfo_dict["size"]

        return nbytes*nelements

    for key,val in data_dict.items():
   
        nelements = get_no_of_elements(val)

        bmin = bmin + fortran_write_nbytes
        bmax = bmin + get_no_of_bytes(val,nelements)

        data = struct.unpack(val["type"] * (nelements),data_bin[bmin:bmax] )

        if (nelements>1) :
            data_reshaped = np.array(data).reshape(tuple(val["shape"]))
            data = data_reshaped

        bmax = bmax + fortran_write_nbytes
        bmin = bmax

        read_data[key] = data

    return read_data 


    

def parse_particle_stats(input_file : str) -> pd.DataFrame:
    '''
    parse particle statistic file 
    generated by Fortan postprocessing routine
    by spectral channel flow code

    Input
    -----
    input_file - path to the input file

    Output
    ------
    particle_stats - pd.DataFrame object
        with column names parsed from the 
        description in the input_file

    Notes
    -----
    input_file is written in HRF, but vary in length
    depending on the version of postprocessing routine

    '''
    description_lines_cntr = 0
    pattern = "^ \% Column (\d+):"
    p = re.compile(pattern)            
    column_names = [] 


    # obtaining names of columns and number of skiprows
    with open(input_file) as f:

        while True:
            d = f.readline()
            try:
                float(d.split()[0])
            except (ValueError, IndexError):
                description_lines_cntr += 1
                if p.match(d):
                    name = d.split(':')[1].split('(')[0].strip()
                    column_names.append(name)
            else:
                break

    skiprows = description_lines_cntr
    particle_stats = pd.read_table(input_file,
                                   delim_whitespace=True, 
                                   skiprows=skiprows,
                                   header=None,
                                   names = column_names)

    return particle_stats
