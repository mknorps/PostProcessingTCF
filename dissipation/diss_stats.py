# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: diss_stats.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 11-01-2018 09:19:43
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
import pandas as pd
import numpy as np

from pplib import parameters as p
from itertools import product


def data_generator(files):

    for fluid_file in files:
        data = pd.read_table(fluid_file,names=f.columns_apriori, delim_whitespace=True, header=None)
        yield data 

def compute_stats(generator_function,files):

    average = 0 
    try:
        average = sum(generator_function(files))/len(files)

    except ZeroDivisionError:
        print("Empty argument - no files listed")

    return average

def write_to_file(file_write):
  
    data_apriori = compute_stats(data_generator,f.files_apriori)
    data_LES = compute_stats(data_generator,f.files_LES)

    data = {'apriori':data_apriori,
            'LES':data_LES}
    data_panel = pd.Panel(data)

    data_panel.to_excel(file_write)

def symmetrise(diss_file,file_write):

    data_symm =  pd.read_excel(diss_file, sheet_name = None)
    symm_columns =list(set(f.columns_apriori) - set(f.asymm_columns)) 

    for s,c in product(f.types,symm_columns):
        lst = data_symm[s][c]
        l = len(lst)
        data_symm[s][c] = 0.5*(lst[:(l+1)//2-1] + np.flipud(lst)[1:(l+1)//2])
    for s,c in product(f.types,f.asymm_columns):
        lst = data_symm[s][c]
        l = len(lst)
        data_symm[s][c] = 0.5*(lst[:(l+1)//2-1] - np.flipud(lst)[1:(l+1)//2])

    for s in ['apriori','LES']:
        data_symm[s]['y'] = (1-data_symm[s]['y'])*p.Retau
    
    data_panel = pd.Panel(data_symm)
    data_panel.to_excel(file_write)

    return data_panel

