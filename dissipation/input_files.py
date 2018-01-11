# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: input_files.py
# Created by: gemusia
# Creation date: 09-01-2018
# Last modified: 11-01-2018 09:17:40
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from os.path import expanduser
from os import  listdir

file_path_main = expanduser("~") + '/results_for_PhD/fluid_dissipation/'

file_path_apriori = file_path_main + "apriori/"
file_path_LES = file_path_main + "LES/"
file_path_write = file_path_main + "dissipation.xls"
file_path_symm = file_path_main + "dissipation_symm.xls"

#lists of files
files_apriori = [file_path_apriori +filename for filename in listdir(file_path_apriori)]
files_LES     = [file_path_LES +filename for filename in listdir(file_path_LES)]

columns_LES = ['y','epsl_tot','trash','epsl_model1','epsl_model2']
columns_apriori = ['y','epsl_tot','epsl_LES','epsl_model1','epsl_model2']
types = ['apriori','LES']
asymm_columns = ['y']
