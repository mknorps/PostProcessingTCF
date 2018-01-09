# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: input_files.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 09-01-2018 18:18:57
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from os.path import expanduser
from os import  listdir

file_path_main = expanduser("~") + '/results_for_PhD/fluid_SGS_velocity/'

file_path_def = file_path_main + "from_definition/"
file_path_apriori = file_path_main + "Yoshizawa_apriori/"
file_path_LES = file_path_main + "Yoshizawa_LES/"

#lists of files
files_def     = [filename for filename in listdir(file_path_def)]
files_apriori = [filename for filename in listdir(file_path_apriori)]
files_LES     = [filename for filename in listdir(file_path_LES)]

columns = ['y','u2sgs_y','u2sgs_z','u2sgs_x','u2sgs_yz','u2sgs_xy','u2sgs_xz']
