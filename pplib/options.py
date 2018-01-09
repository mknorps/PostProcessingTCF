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
        usage='python project -computetau [fluid|heavy]'
        self.parser = ArgumentParser(usage=usage)

        self.parser.add_argument('--slice_yplus','-slice_yplus','--sy','-sy',
                                 dest='slice_yplus',
                                 help='slice of particle field at chosen y+')

        #self.parser.add_argument('ct',help="input for --computetau")

    def parse(self,args=None):
        self.known, self.unknown = self.parser.parse_known_args(args)[:]
        if len(self.unknown) !=0:
            print("WARNING Unknown args received: " + repr(self.unknown))
        return self.known
