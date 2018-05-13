########################################
#
#  written by mknorps, 2018
#
#  draws panel of statistics
#
#  usage: python draw_stats -h
#
########################################

import sys
import csv
from os.path import expanduser
sys.path.insert(0,'/home/mknorps/Projects/ForPhD/PostProcessingTCF/')

from pplib import tcf_parsers

import stat_panels as sp
import options 

# declaration of constants
StList = ['1','5','25']
reference_path_LES  = expanduser("~") +"/REFERENCE_DATA/pure_LES/int2/"
reference_path_DNS  = expanduser("~") +"/REFERENCE_DATA/Marchiolli_DATA/TUE/"



def read_input(input_file):
    
    models = {}
    with open(input_file) as csvfile:
        stat_reader = csv.reader(csvfile)
        headers = next(stat_reader)
        for row in stat_reader:
            models[row[0]]=row[1].strip()

    return models



def run_project(args):

    opt = options.Options()
    parsed_args = opt.parse(args[1:])

    input_file = parsed_args.input_file
    output_file = parsed_args.output_file[0]
    velocity = parsed_args.velocity
    panel = parsed_args.panel

    print(output_file)
    if input_file:
        print ("input file: ",input_file)
        models_input = read_input(input_file)

    # setting default velocity option
    if not velocity:
        velocity='u'

    # setting default velocity option
    if not panel:
        panel='conc'


    panel_choice={'conc':sp.concentration_panel,
                  'ksgs':sp.ksgs_panel}

    models = {} 
    LES = {}
    DNS = {}

    for i,x in enumerate(StList):

        for k,v in models_input.items():
            models[k]=tcf_parsers.parse_particle_stats(v +x) 

        LES[x] =  tcf_parsers.parse_particle_stats(reference_path_LES 
                + 'particle_stat_' + x)
        DNS[x] = tcf_parsers.parse_particle_stats(reference_path_DNS 
                + 'dns_particles_' + x)

        panel_choice[panel]("{}_{}_{}.pdf".format(output_file,velocity,x),
                x,LES,DNS,velocity=velocity,**models)


if __name__=='__main__':

    run_project(sys.argv)
