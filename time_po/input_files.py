# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: input_files.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 12-01-2018 12:13:44
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from os.path import expanduser
from os import  listdir
from collections import OrderedDict
from itertools import product

from pplib import parameters as p

file_path_main = expanduser("~") + '/results_for_PhD/time_po/'

file_path_LES = file_path_main + "LES/"

file_path_write = file_path_main + "upar_stats.csv"
#lists of files
files_LES     = [file_path_LES +filename for filename in listdir(file_path_LES)]

columns = ['y','u2sgs_y','u2sgs_z','u2sgs_x','u2sgs_yz','u2sgs_xy','u2sgs_xz']

VariableList = ['upar','vpar','usgs']
ColumnList = [i[0]+'_'+i[1]  for i in product(VariableList,p.DirectionList)]

data_dict_min = OrderedDict([("t",{"size":4,"type":"integer"}),
            ("time",{"size":8,"type":"real"}),
            ("pos",{"size":8, "shape":[3,p.N],"type":"real"}),
            ("vpar",{"size":8, "shape":[4,p.N],"type":"real"}),
            ("upar",{"size":8, "shape":[4,p.N],"type":"real"}),
            ("usgs",{"size":8, "shape":[3,p.N],"type":"real"})])
