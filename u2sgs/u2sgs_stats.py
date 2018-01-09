# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: u2sgs_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 09-01-2018 18:42:15
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd


def compute_bin_stats_def():

    binned_stats = {}
    for particle_file in f.files_def:

        data_hrf = bff.unpack_particles_file(particle_file,p.data_dict_apriori)
        d = ua.U2sgs(data_hrf)
        df = bu.BinnedTau(d.df)
        binned = df.bin_stat(['usgs_x','usgs_y','usgs_z',
                              'upar_x','upar_y','upar_z',
                              'uparf_x','uparf_y','uparf_z' ])

    return binned_stats

def data_generator(files):

    for fluid_file in files:
        data = pd.read_table(fluid_file,names=f.columns, delim_whitespace=True, header=None)
        yield data 

def compute_bin_stats_model(files):

    try:
        average = sum(data_generator(files))/len(files)
        return average

    except ZeroDivisionError:
        print("Empty argument - no files listed")



def compute_bin_stat_LES():
    compute_bin_stats_model(f.files_LES)
def compute_bin_stat_apriori():
    compute_bin_stats_model(f.files_apriori)


def write_to_file(file_write):
  
    data_def =  compute_bin_stats_def()
    data_apriori =  compute_bin_stat_apriori()
    data_LES =  compute_bin_stat_LES()

    data = {'def':data_def,
            'apriori':data_apriori,
            'LES':data_LES}
    data_panel = pd.Panel(data)

    data_panel.to_excel(file_write)
