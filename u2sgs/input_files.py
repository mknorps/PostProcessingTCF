# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: input_files.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 09-01-2018 13:13:35
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from os.path import expanduser
from os import  listdir

file_path_main = expanduser("~") + '/results_for_PhD/fluid_SGS_velocity/'

file_path_def = file_path_main + "from_definition/"
file_path_apriori = file_path_main + "Yoshizawa_apriori/"
file_path_LES = file_path_main + "Yoshizawa_LES/"

#iterators
files_def     = (filename for filename in listdir(file_path_def))
files_apriori = (filename for filename in listdir(file_path_apriori))
files_LES     = (filename for filename in listdir(file_path_LES))
