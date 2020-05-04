# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:14:25 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem63 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem63(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem63(self):
        problem = otb.ReliabilityProblem63()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.000379
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-15)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0] * 100
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], -4.5)


if __name__ == "__main__":
    unittest.main()
