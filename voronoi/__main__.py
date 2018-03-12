'''
Voronoi tessalation 
-------------------

- draw voronoi polygons
- draws histograms of voronoi cell ares 
    (computed in a separate Octave (program)

'''

import sys
import numpy as np

import voronoi_draw as vd



def run_project(args):
    
    opt = options.Options()

    parsed_args = opt.parse(args[1:])

    slice_file = "/home/gemusia/results_for_PhD/voronoi/slices/LES/slice_LES_St25_4860_left.csv"
    pict_path = "/home/gemusia/results_for_PhD/voronoi/slices/LES/voronoi_snapshot_LES_St25.eps"
    vd.draw_voronoi_from_slice(slice_file, pict_path)

    data_St1 = np.loadtxt("/home/gemusia/kody/voronoi_IMP/hist_FRACTAL_St1.res",skiprows=5)
    data_St5 = np.loadtxt("/home/gemusia/kody/voronoi_IMP/hist_FRACTAL_St5.res",skiprows=5)
    data_St25 = np.loadtxt("/home/gemusia/kody/voronoi_IMP/hist_FRACTAL_St25.res",skiprows=5)

    results_St1 = {'data':data_St1[:,2], 'label':"St1"}
    results_St5 = {'data':data_St5[:,2], 'label':"St5"}
    results_St25 = {'data':data_St25[:,2], 'label':"St25"}
    vd.draw_histogram("Voronoi_his_FRACTAL.eps",data_St1[:,0],data_St1[:,1],
            results_St1, results_St5, results_St25)



if __name__=="__main__":

    run_project(sys.argv)

