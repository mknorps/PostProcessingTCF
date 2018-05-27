import sys
import numpy as np
from itertools import product

import voronoi_draw as vd

from os.path import expanduser
sys.path.insert(0,'/home/mknorps/Projects/ForPhD/PostProcessingTCF/')

from pplib import parameters as p

linestyle_type = {'DNS':{'linestyle':'solid'},
             'LES':{'linestyle':'dashed'},
             'FRACTAL':{'linestyle':'dotted'}
        }
linestyle_Stokes = {'St1':{'color':'blue'},
                    'St5':{'color':'red'},
                    'St25':{'color':'green'}
                    }

def voronoi_hist(pict_file):
    '''
    draw histogram of Voronoi polygons areas
    '''
    data = {}
    #for st,sym_type in product(p.StList_min, p.SymTypes):
    #for st,sym_type in product(['St1','St5','St25'], ['LES','DNS']):
    for st,sym_type in product(['St5'], ['LES','DNS', 'FRACTAL']):
        hist_values =  np.loadtxt(
                "/home/mknorps/Projects/ForPhD/voronoi_IMP/hist_{}_center_{}.dat"
                .format(sym_type,st),skiprows=5)
        sym = sym_type.split('_')[0]
        data["{} {}".format(st,sym)] =[hist_values[:,2], {**linestyle_type[sym], **linestyle_Stokes[st]}]  
        bins = hist_values[:,0]
        theoretical = hist_values[:,1]


    vd.draw_histogram(pict_file,
            bins, theoretical, **data)



def run_project(args):
    
    #draw voronoi tessalation
    it = {'DNS':2620, 'LES':4860,'FRACTAL':880}
    for s,x in product(['DNS','LES', 'FRACTAL'],[1,5,25]):
        slice_file = "/home/gemusia/results_for_PhD/voronoi/slices/{}/slice_{}_center_St{}_{}_left.csv".format(s,s,x,it[s])
        pict_path = "/home/gemusia/results_for_PhD/voronoi/slices/{}/voronoi_snapshot_{}_center_St{}.eps".format(s,s,x)
        vd.draw_voronoi_from_slice(slice_file, pict_path)



if __name__=="__main__":

    #run_project(sys.argv)
    voronoi_hist("/home/mknorps/Projects/ForPhD/voronoi_IMP/hist_FRACTAL_center_voronoi.eps")

