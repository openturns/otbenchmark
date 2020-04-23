# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:32:41 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem31 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem31(unittest.TestCase):

    def test_ReliabilityBenchmarkProblem31(self):
        problem = otb.ReliabilityProblem31()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.00018
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.e-15)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert(type(Y) is ot.Point)
        np.testing.assert_allclose(Y[0], 2)


if __name__ == "__main__":
    unittest.main()

