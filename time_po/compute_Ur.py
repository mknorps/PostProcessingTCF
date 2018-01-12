# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: compute_Ur.py
# Created by: gemusia
# Creation date: 12-01-2018
# Last modified: 12-01-2018 13:56:26
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import input_files as f
from pplib import parameters as p


from pplib import binary_from_fortran as bff
from pplib import particles as par
from pplib import compute_stats as cs


def particle_generator(files):

    for particle_file in files:
        data_hrf = bff.unpack_particles_file(particle_file,f.data_dict_min)
        df = par.Particles(data_hrf,columns=f.ColumnList)

        for d in p.DirectionList:
            df.new_column('ur_'+d,lambda x,y: x-y, ['vpar_'+d,'upar_'+d])

        print(df.describe())

        binned = df.bin_stat(['ur_x','ur_y','ur_z','upar_x','vpar_x'])
        yield binned 

def write_to_file(file_write):

    data = cs.compute_stats(particle_generator,f.files_LES)

    data.to_csv(file_write)


