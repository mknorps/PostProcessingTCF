import sys
import numpy as np
from itertools import product

import voronoi_draw as vd
from pplib import parameters as p

def voronoi_hist(pict_file):
    '''
    draw histogram of Voronoi polygons areas
    '''
    data = {}
    for st,sym_type in product(p.StList_min, p.SymTypes):
    #for st,sym_type in product(['St1','St5','St25'], ['LES','DNS']):
        hist_values =  np.loadtxt(
                "/home/gemusia/kody/voronoi_IMP/hist_{}_{}.res"
                .format(sym_type,st),skiprows=5)
        data["{} {}".format(st,sym_type)] =hist_values[:,2]  
        bins = hist_values[:,0]
        theoretical = hist_values[:,1]


    vd.draw_histogram(pict_file,
            bins, theoretical, **data)



def run_project(args):
    
    #draw voronoi tessalation
    slice_file = "/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_St25_4860_left.csv"
    pict_path = "/home/gemusia/results_for_PhD/voronoi/slices/LES/voronoi_snapshot_LES_St25.eps"
    vd.draw_voronoi_from_slice(slice_file, pict_path)



if __name__=="__main__":

    run_project(sys.argv)
    voronoi_hist("/home/gemusia/results_for_PhD/voronoi/hist_LES_DNS_FRACTAL_voronoi.eps")

