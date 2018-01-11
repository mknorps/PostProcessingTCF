# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 10-01-2018 15:19:35
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np


from pplib import binary_from_fortran as bff
from pplib import parameters as p
import u2sgs_apriori as ua


def particle_generator(files):

    for particle_file in files:
        data_hrf = bff.unpack_particles_file(particle_file,p.data_dict_apriori)
        df = ua.U2sgs(data_hrf)
        binned = df.bin_stat(['usgs_x','usgs_y','usgs_z','cov_xy'], covariances=[['usgs_x','usgs_y'],['usgs_x','usgs_z'],['usgs_y','usgs_z']])
        yield binned 

def data_generator(files):

    for fluid_file in files:
        data = pd.read_table(fluid_file,names=f.columns, delim_whitespace=True, header=None)
        yield data 

def compute_stats(generator_function,files):

    average = 0 
    try:
        average = sum(generator_function(files))/len(files)

    except ZeroDivisionError:
        print("Empty argument - no files listed")

    return average



def compute_bin_stat_LES():
    return compute_stats(data_generator,f.files_LES)
def compute_bin_stat_apriori():
    return compute_stats(data_generator,f.files_apriori)
def compute_bin_stat_def():
    return compute_stats(particle_generator,f.files_def)


def write_to_file(file_write):
  
    data_def =  compute_bin_stat_def()
    data_apriori =  compute_bin_stat_apriori()
    data_LES =  compute_bin_stat_LES()

    data = {'def':data_def,
            'apriori':data_apriori,
            'LES':data_LES}
    data_panel = pd.Panel(data)

    data_panel.to_excel(file_write)
