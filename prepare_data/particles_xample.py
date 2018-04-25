# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: particles_xample.py
# Created by: gemusia
# Creation date: 17-04-2018
# Last modified: 19-04-2018 10:08:04
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas as pd
from pplib import particles as par
from pplib import tcf_parsers as tp
from pplib import parameters as p


input_dir = "/home/gemusia/results_for_PhD/IntegrationSchemes/ParticleFields/"

rk2_dict = tp.unpack_particles_file(input_dir + "RK2_WALLDEP_particles_4980", 
        p.data_dict_LES)
rk2 = {key: rk2_dict[key] for key in ['pos','upar','vpar']}

exp1_dict = tp.unpack_particles_file(input_dir + "EXP_WALLDEP_particles_4980", 
        p.data_dict_LES)
exp1 = {key: exp1_dict[key] for key in ['pos','upar','vpar']}


rk2_df = par.Particles(rk2, columns = ['upar_x','upar_y','upar_z','vpar_x','vpar_y','vpar_z'])
exp1_df = par.Particles(exp1, columns = ['upar_x','upar_y','upar_z','vpar_x','vpar_y','vpar_z'])

rk2_df.to_csv(input_dir+'rk2_walldep_df.csv')
exp1_df.to_csv(input_dir+'exp1_walldep_df.csv')

