###############################################
#
#  mknorps, 11.11.2017
#
#  script for convergence check of particles 
#         simulations
#
#
###############################################

import numpy as np
from collections import OrderedDict
from os.path import expanduser

N     = 400000
N_par = 100000 #number of particles of one kind
utau = 0.0429
Retau = 150
ttau = 1.0/(utau*Retau)
StList = ['St0.2','St1','St5','St25']
DirectionList=['x','y','z']


line_style_dict = {"fluid": {"ls":"solid", "color":"blue", "label":"fluid","lw":2},
                   "St0.2":  {"ls":"solid", "color":"purple", "label":"$St0.2$","lw":2},
                   "St1":   {"ls":"solid", "color":"green", "label":"$St1$","lw":2},
                   "St5":   {"ls":"solid", "color":"red", "label":"$St5$","lw":2},
                   "St25":  {"ls":"solid", "color":"orange", "label":"$St25$","lw":2},
                   "St125": {"ls":"solid", "color":"black", "label":"$St125$","lw":2},
} 


# bins for histograms are taken according to eros of Chebyshev
#      polynomials
N_bins = 16
def y(j):
    return np.cos(float(j)*np.pi/float(N_bins))

def y_plus(y):
    return Retau * (y+1) 

def Chebyshev_zeroes(N):
    return 0.5*(np.array(range(1,N+1))+np.array(range(N)))/N * Retau


bins = list(reversed([y(j)*Retau for j in range(N_bins//2+1 )]))
bins_y = np.array(list(reversed([y(j) for j in range(N_bins+1)])))
bins_centers = 0.5*(bins_y[:N_bins]+bins_y[1:])

# file structure
# files are written in fortran with :
'''
       write(3)t
       write(3)time
       write(3)pos
       write(3)vpar
       write(3)upar
       write(5)usgs
       write(3)tausg1

fortran inserts integer*4 byte at beginning and end of each unformatted wrie statement

t        : integer
time     : real*8
pos,usgs : real*8 [400000,3]
vpar,upar: real*8 [400000,4]

400000 particles - 4 types of particles 100000 of each

'''
data_dict3 = OrderedDict([("t",{"size":4,"type":"integer"}),
            ("time",{"size":8,"type":"real"}),
            ("pos",{"size":8, "shape":[3,N],"type":"real"}),
            ("vpar",{"size":8, "shape":[4,N],"type":"real"}),
            ("upar",{"size":8, "shape":[4,N],"type":"real"}),
            ("usgs",{"size":8, "shape":[3,N],"type":"real"}),
            ("uparf",{"size":8, "shape":[4,N],"type":"real"})])

data_dict2 = OrderedDict([("t",{"size":4,"type":"integer"}),
            ("time",{"size":8,"type":"real"}),
            ("pos",{"size":8, "shape":[N,3],"type":"real"}),
            ("vpar",{"size":8, "shape":[N,4],"type":"real"}),
            ("upar",{"size":8, "shape":[N,4],"type":"real"}),
            ("usgs",{"size":8, "shape":[N,3],"type":"real"})])

data_dict = OrderedDict([("t",{"size":4,"type":"integer"}),
            ("time",{"size":8,"type":"real"}),
            ("pos",{"size":8, "shape":[3,N],"type":"real"}),
            ("vpar",{"size":8, "shape":[4,N],"type":"real"}),
            ("upar",{"size":8, "shape":[4,N],"type":"real"}),
            ("usgs",{"size":8, "shape":[3,N],"type":"real"}),
            ("tausg1",{"size":8, "shape":[1,N],"type":"real"}),
            ("tausg2",{"size":8, "shape":[3,N],"type":"real"})]) 

# file paths 
file_path_main = expanduser("~") + '/wyniki/time_scales_modelled/'
file_path_data = file_path_main + 'from_tryton/'
file_path_computed = file_path_main + 'computed_model/'
file_path_apriori = expanduser("~") + "/wyniki/time_scales_ii/"
f_name_tau = file_path_apriori + "tau.csv"
