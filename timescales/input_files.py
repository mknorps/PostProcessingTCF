# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: input_files.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 21-01-2018 12:30:17
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from os.path import expanduser
from os import  listdir
from collections import OrderedDict
from itertools import product

from pplib import parameters as p


file_path_main = expanduser("~") + '/wyniki/time_scales_modelled/from_tryton/'

file_path_tau_sg = file_path_main + "tau_sg_no_directions/"
data_path = expanduser("~") + "/results_for_PhD/timescales/"
file_path_write = data_path + "tau_sg_models.csv"
file_path_write_symm = data_path + "tau_sg_models_symm.csv"

#lists of files
files_tau_sg     = [file_path_tau_sg + filename for filename in listdir(file_path_tau_sg)]

columns = ['y','tausg2_0','tausg2_1', 'tausg2_2']

asymm_columns = ['y']

norm_factor = {v:p.ttau for v in columns if v!='y'}
norm_factor['y'] = 1.0


data_dict_LES = OrderedDict([("t",{"size":4,"type":"integer"}),
            ("time",{"size":8,"type":"real"}),
            ("pos",{"size":8, "shape":[3,p.N],"type":"real"}),
            ("vpar",{"size":8, "shape":[4,p.N],"type":"real"}),
            ("upar",{"size":8, "shape":[4,p.N],"type":"real"}),
            ("usgs",{"size":8, "shape":[3,p.N],"type":"real"}),
            ("tausg1",{"size":8, "shape":[1,p.N],"type":"real"}),
            ("tausg2",{"size":8, "shape":[3,p.N],"type":"real"}),
])
