# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: test_optimize.py
# Created by: gemusia
# Creation date: 22-12-2017
# Last modified: 26-01-2018 16:13:36
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import unittest
import numpy as np
import pandas as pd

from pplib import slice_concentration as sc

from hypothesis import given,reproduce_failure
from hypothesis.extra.numpy import *
import hypothesis.strategies as st

clist = ['x','y','z']
L = 100000
vallist_zeros = [2*np.pi*np.random.random_sample(L),np.ones(L),np.pi*np.random.random_sample(L)]

s = sc.SliceConc(dict(zip(clist,vallist_zeros)))
print (type(s))

class SliceConcTests(unittest.TestCase):

    def test_conc_histogram(self):
        h1 = s.conc_histogram([100,100])
        h2 = s.conc_histogram([50,50])
        self.assertAlmostEqual(h1,h2)


if __name__=='__main__':
    unittest.main()
