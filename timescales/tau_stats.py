# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: tau_stats.py
# Created by: gemusia
# Creation date: 21-01-2018
# Last modified: 09-04-2018 14:02:12
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import input_files as f
import pandas as pd
import numpy as np
from itertools import product


from pplib import tcf_parsers 
from pplib import parameters as p
from pplib import particles as par 
from pplib import compute_stats as cs
from pplib import optimize as o


def tausg_generator(files):

    for particle_file in files:
        data_hrf = tcf_parsers.unpack_particles_file(particle_file,f.data_dict_LES)
        df = par.Particles(data_hrf,columns_tau=['tausg2'])       
 
        binned = df.bin_stat(f.columns, norm_factor = f.norm_factor)
        yield binned

def compute_bin_stat_tau_sg():
    return cs.compute_stats(tausg_generator,f.files_tau_sg)

def symmetrise():

    data_tau = compute_bin_stat_tau_sg()

    symm_columns =list(set(data_tau.columns) - set(f.asymm_columns))
    data_symm = pd.DataFrame() 
    for c in symm_columns:
        lst = data_tau[c]
        l = len(lst)
        data_symm[c] = 0.5*(lst[:(l+1)//2-1] + np.flipud(lst)[1:(l+1)//2])
    for c in f.asymm_columns:
        lst = data_tau[c]
        l = len(lst)
        data_symm[c] = 0.5*(lst[:(l+1)//2-1] - np.flipud(lst)[1:(l+1)//2])

    data_symm['y'] = (1+data_symm['y'])*p.Retau

    return data_symm


def optimize_tau_fluid(input_file=''):

    reference_data_file = f.data_path + "tau_ii.csv"
    reference_data = pd.read_csv(reference_data_file)

    mean_tausg = (reference_data['fluid_SGSles_x']\
                 +reference_data['fluid_SGSles_y']\
                 +reference_data['fluid_SGSles_z'])/3
    mean_tausg_interpolated = [[x,0.5*(x+y)] for (x,y) in zip (mean_tausg[:-1],mean_tausg[1:])]
    mean_tausg_interpolated = np.array(mean_tausg_interpolated)
    l = (len(mean_tausg)-1)*2
    mean_tausg_interpolated = mean_tausg_interpolated.reshape(l)
    mean_tausg_interpolated = np.append(mean_tausg_interpolated,mean_tausg[len(mean_tausg)-1])

    if input_file != '':
        data_tau = pd.read_csv(input_file)
    else:
        data_tau = symmetrise()
   
    optimal =  o.fit_data_series(data_tau['tausg2_1'][1:],mean_tausg_interpolated[1:])
    print(optimal)
    return optimal


def write_to_file(file_write, symm = True):

    if symm==True:
        data_tau = symmetrise() 
    else:
        data_tau = compute_bin_stat_tau_sg()

    data_tau.to_csv(file_write)
