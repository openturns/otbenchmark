# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:50:49 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem14 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem14(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem14(self):
        problem = otb.ReliabilityProblem14()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.00752
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-15)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 1.0, 0.0, 0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 0.0)


if __name__ == "__main__":
    unittest.main()
