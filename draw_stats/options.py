# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: options.py
# Created by: gemusia
# Creation date: 16-12-2017
# Last modified: 29-12-2017 14:10:02
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from argparse import ArgumentParser

class Options:

    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage='python draw_stats output_name -i input_file'  
        self.parser = ArgumentParser(usage=usage)

        self.parser.add_argument('output_file', nargs=1,
                                 help='core of the output file name for panel of statistics figures')

        self.parser.add_argument('-i',
                                 dest='input_file',
                                 help='input file with list of particle statistics file paths')

        self.parser.add_argument('-velocity',
                                 dest='velocity', choices=['u','v'],
                                 help='type of velocity: u (fluid), v (particle)')


        self.parser.add_argument('-panel',
                                 dest='panel', choices=['conc','ksgs'],
                                 help='type of drawn panel: conc (concentration), ksgs (kinetic energy)')


    def parse(self,args=None):
        self.known, self.unknown = self.parser.parse_known_args(args)[:]
        if len(self.unknown) !=0:
            print("WARNING Unknown args received: " + repr(self.unknown))
        return self.known
