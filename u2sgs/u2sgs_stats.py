# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 12-01-2018 11:21:56
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np


from pplib import binary_from_fortran as bff
from pplib import parameters as p
from pplib import particles as par
from pplib import compute_stats as cs


def particle_generator(files):

    for particle_file in files:
        data_hrf = bff.unpack_particles_file(particle_file,f.data_dict_apriori)
        df = par.Particles(data_hrf,columns=f.ColumnList)
        for d in p.DirectionList:
            df.new_column('usgs_'+d,lambda x,y: x-y, ['upar_'+d,'uparf_'+d])

        binned = df.bin_stat(['usgs_x','usgs_y','usgs_z'], covariances=[['usgs_x','usgs_y'],['usgs_x','usgs_z'],['usgs_y','usgs_z']])
        yield binned 

def data_generator(files):

    for fluid_file in files:
        data = pd.read_table(fluid_file,names=f.columns, delim_whitespace=True, header=None)
        yield data 


def compute_bin_stat_LES():
    return cs.compute_stats(data_generator,f.files_LES)
def compute_bin_stat_apriori():
    return cs.compute_stats(data_generator,f.files_apriori)
def compute_bin_stat_def():
    return cs.compute_stats(particle_generator,f.files_def)


def write_to_file(file_write):
  
    data_def =  compute_bin_stat_def()
    data_apriori =  compute_bin_stat_apriori()
    data_LES =  compute_bin_stat_LES()

    data = {'def':data_def,
            'apriori':data_apriori,
            'LES':data_LES}
    data_panel = pd.Panel(data)

    data_panel.to_excel(file_write)
