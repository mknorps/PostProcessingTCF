# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: test_optimize.py
# Created by: gemusia
# Creation date: 22-12-2017
# Last modified: 28-02-2018 21:55:45
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import unittest
import numpy as np
import pandas as pd

from pplib import halo as hl

from hypothesis import given,reproduce_failure
from hypothesis.extra.numpy import *
import hypothesis.strategies as st



class HaloTests(unittest.TestCase):

    def test_zero_offset(self):
        df = pd.DataFrame({'x':np.arange(100),
                          'y':np.arange(100)})
        df_halo = hl.points_with_halo(df,'x','y',0)
        self.assertTrue(df.equals(df_halo))

    
    def test_signle_point_offset(self):
        df = pd.DataFrame({'x':np.arange(100),
                          'y':np.arange(100)})
        df_halo = hl.points_with_halo(df,'x','y',0.0099)
        df.loc[100] = [99,0]
        df.loc[101] = [0,99]
        self.assertTrue(df.equals(df_halo))

    def test_df_range(self):
        df = pd.DataFrame({'x':np.arange(101),
                          'y':np.arange(101)})
        df_halo = hl.points_with_halo(df,'x','y',0.5)
        self.assertAlmostEqual(min(df_halo['x']),-49)
        self.assertAlmostEqual(max(df_halo['x']),149)
        self.assertAlmostEqual(min(df_halo['y']),-49)
        self.assertAlmostEqual(max(df_halo['y']),149)



if __name__=='__main__':
    unittest.main()
