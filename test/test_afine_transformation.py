# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# File name: test_optimize.py
# Created by: gemusia
# Creation date: 22-12-2017
# Last modified: 26-01-2018 16:28:48
# Purpose: 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import unittest
import numpy as np
import pandas as pd

from pplib import afine_transformation as at

from hypothesis import given,reproduce_failure
from hypothesis.extra.numpy import *
import hypothesis.strategies as st



class FractalInterpolationOneIntervalTests(unittest.TestCase):

    def test_constant(self):
        U = (1,1,1)
        d1=1
        d2=1
        fractal = at.w(U,d1,d2,1)(1)
        self.assertAlmostEqual(U[1],fractal(0.5))

    def test_u0(self):
        U = (1,4,3)
        d1=1
        d2=1
        fractal = at.w(U,d1,d2,0)(1)
        self.assertAlmostEqual(fractal(0.5),2)

    def test_w1_u0(self):
        U = (1,4,3)
        d1=1
        d2=1
        fractal = at.w(U,d1,d2,1)(1)
        self.assertAlmostEqual(fractal(0.5),4)

    def test_w1_u0_1(self):
        U = (1,4,3)
        d1=2
        d2=2
        fractal = at.w(U,d1,d2,1)(1)
        self.assertAlmostEqual(fractal(0.5),4)


class FractalInterpolationTests(unittest.TestCase):

    def test_constant(self):
        U = (1,1,1,1,1)
        d1=2
        d2=2
        fractal = [at.w(U,d1,d2,1)(i) for i in [1,2]]
        self.assertAlmostEqual(U[1],fractal[0](0.5))
        self.assertAlmostEqual(U[1],fractal[1](0.5))
        

    def test_linear(self):
        U = (1,2,3,4,5)
        d1=2
        d2=2
        fractal = [at.w(U,d1,d2,1)(i) for i in [1,2]]
        self.assertAlmostEqual(U[1],fractal[0](0.5))
        self.assertAlmostEqual(U[3],fractal[1](0.5))

if __name__=='__main__':
    unittest.main()
